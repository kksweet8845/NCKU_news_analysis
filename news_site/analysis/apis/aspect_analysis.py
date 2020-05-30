import torch
import pandas as pd
from transformers import BertTokenizer
import json
from django.conf import settings
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence
from transformers import BertForSequenceClassification
from tqdm import tqdm
import re

util_path = settings.BASE_DIR + '/analysis/apis/utils/aspect_data'



def get_predictions(model, dataloader, compute_acc=False):
        predictions = None
        correct = 0
        total = 0
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        trange = tqdm(dataloader, total=len(dataloader))
        ids = None
        with torch.no_grad():
            # 遍巡整個資料集
            for data in trange:
                # 將 tenosrs 移到 GPU 上
                if next(model.parameters()).is_cuda:
                    data = [t.to(device) for t in data if t is not None]
                # 別忘記前 3 個 tensors 分別為 tokens, segments 以及 masks
                if not compute_acc:
                    tokens_tensors, segments_tensors, masks_tensors, _, id = data[:]
                else:
                    tokens_tensors, segments_tensors, masks_tensors = data[:3]
                outputs = model(input_ids=tokens_tensors, token_type_ids=segments_tensors, attention_mask=masks_tensors)

                logits = outputs[0]
                _, pred = torch.max(logits.data, 1)
                # 用來計算訓練集的分類準確率
                if compute_acc:
                    labels = data[3]
                    total += labels.size(0)
                    correct += (pred == labels).sum().item()

                # 紀錄當前 batch
                if predictions is None:
                    predictions = pred
                    ids = id
                else:
                    predictions = torch.cat((predictions, pred))
                    ids = torch.cat((ids, id))

            if compute_acc:
                acc = correct / total
                return predictions, acc
            assert len(predictions) == len(ids)
            return list(zip(predictions.tolist(), ids.tolist()))




class AspectModule:
    def __init__(self, df, mode, batch_size=1):
        self.PRETRAINED_MODEL_NAME = "bert-base-chinese"
        self.NUM_LABELS = 3
        self.tokenizer = BertTokenizer.from_pretrained(self.PRETRAINED_MODEL_NAME)
        print("Pytorch version : ", torch.__version__)
        self.vocab = self.tokenizer.vocab
        print("Dictionary size : ", len(self.vocab))
        ## train dataset
        if mode == 'train':
            # self.train_df = pd.read_csv(util_path + '/chineseGLUE/inews/train.txt', sep='_!_', encoding='utf-8')
            self.train_df = df
            self.train_df.dropna()
            self.train_df.drop('id', axis=1, inplace=True)
            self.train_df = self.train_df[['title', 'content', 'label']]
            # self.train_df.to_csv(util_path + '/chineseGLUE/inews/train_tc.csv')
            self.sentimentDataset = self.SentimentDataset(self.train_df, 'train', self.tokenizer)
        elif mode == 'eval':
            self.train_df = None
            self.sentimentDataset = self.SentimentDataset(df, 'eval', self.tokenizer)
        self.BATCH_SIZE = batch_size
        self.loader = DataLoader(self.sentimentDataset,
                                 batch_size=self.BATCH_SIZE,
                                 collate_fn=self.create_mini_batch
                                )

        # model
        self.bertModel = self.Model(self.PRETRAINED_MODEL_NAME, self.NUM_LABELS)



    def create_mini_batch(self, samples):
        tokens_tensors = [s[0] for s in samples]
        segments_tensors = [s[1] for s in samples]

        # 測試集有 labels
        if samples[0][2] is not None:
            label = torch.stack([s[2] for s in samples])
        else:
            label = None

        ids = torch.tensor([ s[3] for s in samples ])

        # zero pad 到同一長度
        tokens_tensors = pad_sequence(tokens_tensors, batch_first=True)
        segments_tensors = pad_sequence(segments_tensors, batch_first=True)

        # attention masks，將 tokens_tensors 裡頭不為 zero padding
        # 的位置設為 1 讓 BERT 只關注這些位置的 tokens
        masks_tensors = torch.zeros(tokens_tensors.shape, dtype=torch.long)
        masks_tensors = masks_tensors.masked_fill(tokens_tensors != 0, 1)

        return tokens_tensors, segments_tensors, masks_tensors, label, ids



    def train(self):
        self.bertModel.train(self.loader)

    def eval(self, ckpt):
        return self.bertModel.eval(ckpt, self.loader)


    def get_learnable_params(self, module):
        return [p for p in module.parameters() if p.requires_grad]

    class SentimentDataset(Dataset):
        def __init__(self, df, mode, tokenizer, max_len=512):
            assert mode in ['train', 'eval']
            self.mode = mode
            try:
                self.df = df
                print(self.df.iloc[136,:].values)
                print(self.df.iloc[137, :].values)
            except FileNotFoundError as err:
                print(err)
                exit()
            self.len = len(self.df)
            self.tokenizer = tokenizer
            self.max_len = max_len

        def __getitem__(self, idx):
            if self.mode == 'train' or self.mode == 'valid':
                title, content, label = self.df.iloc[idx, :].values
                label_tensor = torch.tensor(label)
                id = None
            if self.mode == "test" or self.mode == "eval":
                title, content, id = self.df.iloc[idx, :].values
                label_tensor = None
            # 建立 title 的 BERT tokens 並加入分隔符號 [SEP]
            word_pieces = ['[CLS]']
            tokens_title = self.tokenizer.tokenize(title)
            word_pieces += tokens_title + ['[SEP]']
            len_title = len(word_pieces)

            # 建立 content 的 BERT tokens 並加入分隔符號 [SEP]
            try:
                content = re.sub(r'[0-9]+', '', content)
            except:
                print(self.df.iloc[idx, :].values)
                print(id)
                print(content)
            tokens_content = self.tokenizer.tokenize(content)
            word_pieces += tokens_content + ['[SEP]']
            if len(word_pieces) > self.max_len:
                word_pieces = word_pieces[:self.max_len]
            len_content = len(word_pieces) - len_title

            # 將整個 token 序列轉換成索引序列
            ids = self.tokenizer.convert_tokens_to_ids(word_pieces)
            tokens_tensor = torch.tensor(ids)

            # 將 tiel 包含 [SEP] 的 token 位置設為 0，其他為 1 表示 content
            segments_tensor = torch.tensor([0] * len_title + [1] * len_content, dtype=torch.long)


            return (tokens_tensor, segments_tensor, label_tensor, id)

        def __len__(self):
            return self.len



    class Model:
        def __init__(self, name, num_labels, epoch=3):
            self.model = BertForSequenceClassification.from_pretrained(
                    name, num_labels=num_labels)
            self.model_console()
            self.optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-5)
            self.EPOCH = epoch
            self.NAME = name


        def model_console(self):
            print("""
            name            module
            ----------------------""")
            for name, module in self.model.named_children():
                if name == "bert":
                    for n, _ in module.named_children():
                        print(f"{name}:{n}")
                else:
                    print("{:15} {}".format(name, module))

        def train(self, trainloader):
            self.model.train()

            for epoch in range(self.EPOCH):
                running_loss = 0.0

                for data in trainloader:
                    tokens_tensors, segments_tensors, masks_tensors, labels = [t.to(device) for t in data]
                    # 將參數梯度歸零
                    self.optimizer.zero_grad()

                    # forward pass
                    outputs = self.model(input_ids=tokens_tensors,
                                    token_type_ids=segments_tensors,
                                    attention_mask=masks_tensors,
                                    labels=labels)
                    loss = outputs[0]
                    # backward
                    loss.backward()
                    optimizer.step()
                    # 紀錄當前 batch loss
                    running_loss += loss.item()
                # 計算準確率
                _, acc = get_predictions(self.model, trainloader, compute_acc=True)
                print('[epoch %d] loss: %.3f, acc: %.3f' % (epoch+1, running_loss, acc))

                torch.save(self.model.state_dict(), util_path + f'/model_checkpoints/{self.NAME}-e-{epoch}.ckpt')


        def eval(self, ckpt, evalloader):
            self.model.load_state_dict(torch.load(util_path + '/model_checkpoints/' + ckpt, map_location=torch.device('cpu')))
            device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
            print('device', device)
            self.model = self.model.to(device)
            result = get_predictions(self.model, evalloader, compute_acc=False)

            return result
