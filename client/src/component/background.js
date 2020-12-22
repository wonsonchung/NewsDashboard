import React, { useEffect } from 'react';
import AppBar from '@material-ui/core/AppBar';
import LibraryBooksIcon from '@material-ui/icons/LibraryBooks';
import CssBaseline from '@material-ui/core/CssBaseline';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { createMuiTheme, makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import {NAVER_COLOR} from '../models/colors';
import '../index.css';

function Background(){
    const classes = useStyles();
    const words = [
        {
          text: 'told',
          value: 64,
        },
        {
          text: 'mistake',
          value: 11,
        },
        {
          text: 'thought',
          value: 16,
        },
        {
          text: 'bad',
          value: 17,
        },
      ]
    return(
        <>
        <CssBaseline />
        <AppBar position="relative" style={{ background: NAVER_COLOR }}>
            <Toolbar>
            <LibraryBooksIcon className={classes.icon} />
            <Typography variant="h6" color="inherit" noWrap >YBIGTA NEWS DASHBOARD</Typography>
            </Toolbar>
        </AppBar>
        <main>
            <div className={classes.heroContent}>
                <Container maxWidth="sm">
                    <Typography component="h1" variant="h2" color="textPrimary" align="left">
                        NEWSDASHBOARD
                    </Typography>
                    <Typography variant="h6"  color="textSecondary" align="center">
                        <br/><br/>2020년 12월 23일
                    </Typography>
                </Container>
                
            </div>
        </main>
        </>
    );
}


const useStyles = makeStyles((theme) => ({
    icon: {
      marginRight: theme.spacing(2),
    },
    heroContent: {
      backgroundColor: theme.palette.background.paper,
      padding: theme.spacing(8, 0, 6),
      
    },
    heroButtons: {
      marginTop: theme.spacing(4),
    },  
    cardGrid: {
      paddingTop: theme.spacing(8),
      paddingBottom: theme.spacing(8),
    },
    card: {
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
    },
    cardMedia: {
      paddingTop: '56.25%', // 16:9
    },
    cardContent: {
      flexGrow: 1,
    },
    footer: { 
      backgroundColor: theme.palette.background.paper,
      padding: theme.spacing(6),
    },
  }));

  export default Background;