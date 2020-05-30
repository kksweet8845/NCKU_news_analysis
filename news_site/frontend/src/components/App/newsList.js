import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Divider from '@material-ui/core/Divider';
import InboxIcon from '@material-ui/icons/Inbox';
import DraftsIcon from '@material-ui/icons/Drafts';
import Grid from '@material-ui/core/Grid';
import { shadows } from '@material-ui/system';
import Box from '@material-ui/core/Box';
import PieChart from '../common/pieChart'

const useStyles = makeStyles((theme) => ({
    root: {
        width: '100%',
        height: '50vh',
        backgroundColor: theme.palette.background.paper,
    },
    border: {
        height: '40vh',
        margin: '10vh auto',
    }
}));

export default function SelectedListItem() {
  const classes = useStyles();
  const [selectedIndex, setSelectedIndex] = React.useState(1);

  const handleListItemClick = (event, index) => {
    setSelectedIndex(index);
  };

  return (
    <Grid container className={classes.root} justify="center" spacing={1}>
        <Grid item xs={3}>
            <Box className={classes.border} boxShadow={2}>
                <Grid containerjustify="center" spacing={1}>
                    <Grid item xs={6}>
                        <PieChart
                            grades = {[3.51, 2, 6.18]}
                            nodeId = {'positive'}
                        />
                    </Grid>
                </Grid>
            </Box>
        </Grid>
        <Grid item xs={3}>
            <Box className={classes.border} boxShadow={2}>
                <List component="nav" aria-label="secondary mailbox folder">
                    <ListItem
                    button
                    selected={selectedIndex === 0}
                    onClick={(event) => handleListItemClick(event, 2)}
                    >
                    <ListItemText primary="新聞1" />
                    </ListItem>
                    <Divider />
                    <ListItem
                    button
                    selected={selectedIndex === 1}
                    onClick={(event) => handleListItemClick(event, 3)}
                    >
                    <ListItemText primary="新聞2" />
                    </ListItem>
                    <Divider />
                    <ListItem
                    button
                    selected={selectedIndex === 2}
                    onClick={(event) => handleListItemClick(event, 3)}
                    >
                    <ListItemText primary="新聞2" />
                    </ListItem>
                    <Divider />
                    <ListItem
                    button
                    selected={selectedIndex === 3}
                    onClick={(event) => handleListItemClick(event, 3)}
                    >
                    <ListItemText primary="新聞2" />
                    </ListItem>
                </List>
            </Box>
        </Grid>
        <Grid item xs={3}>
            <Box className={classes.border} boxShadow={2}>
                <List component="nav" aria-label="secondary mailbox folder">
                    <ListItem
                    button
                    selected={selectedIndex === 0}
                    onClick={(event) => handleListItemClick(event, 2)}
                    >
                    <ListItemText primary="新聞1" />
                    </ListItem>
                    <Divider />
                    <ListItem
                    button
                    selected={selectedIndex === 1}
                    onClick={(event) => handleListItemClick(event, 3)}
                    >
                    <ListItemText primary="新聞2" />
                    </ListItem>
                    <Divider />
                    <ListItem
                    button
                    selected={selectedIndex === 2}
                    onClick={(event) => handleListItemClick(event, 3)}
                    >
                    <ListItemText primary="新聞2" />
                    </ListItem>
                    <Divider />
                    <ListItem
                    button
                    selected={selectedIndex === 3}
                    onClick={(event) => handleListItemClick(event, 3)}
                    >
                    <ListItemText primary="新聞2" />
                    </ListItem>
                </List>
            </Box>
        </Grid>
    </Grid>
  );
}
