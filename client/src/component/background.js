import React, { useEffect, useState } from 'react';
import AppBar from '@material-ui/core/AppBar';
import LibraryBooksIcon from '@material-ui/icons/LibraryBooks';
import CssBaseline from '@material-ui/core/CssBaseline';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import {NAVER_COLOR} from '../models/colors';
import ReactWordcloud from 'react-wordcloud';
import DayPicker from 'react-day-picker';
import 'react-day-picker/lib/style.css';
import {WORD} from './Word';
import Moment from 'react-moment';

function Background(){
    const classes = useStyles(); 
    const [startDate, setStartDate] = useState(new Date()); 
    const words = WORD;
    const options = {
      rotations: 2,
      rotationAngles: [0, 0],
      fontSizes:[50,100],
    };
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
                <Container className={classes.flexdi} maxWidth="md">
                    <Container className={classes.top_content}>
                        <Typography component="h1" variant="h2" align='left' color="textPrimary" >
                            NEWSDASHBOARD
                        </Typography>
                        <div className={classes.wc}>
                          <ReactWordcloud words={words} options={options} />
                        </div>
                    </Container>
                    <Container className={classes.second_content}>
                      <div>
                        <DayPicker 
                        selected={startDate}
                        onChange={date => setStartDate(date)} />
                      </div>
                    </Container>
                </Container>
                <Container maxWidth="md">
                    <div className={classes.dateChild}>
                      <Typography>
                        <Moment format="YYYY년 MM월 DD일" date={startDate} />
                      </Typography>  
                    </div>
                    <div>
                      <Typography align='right' color="textSecondary">오후 8시 30분 업데이트</Typography>
                    </div>
                  {/* </Container> */}
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
    flexdi: {
    //   flexDirection: 'row',
        display:'flex',
    },
    top_content: {
        margin:"auto",
        width:'65%',
    },
    second_content: {
        margin:"auto",
        width:'35%',
    },
    wc: {
      margin:"auto",  
      marginTop:'30px',
      width:"90%",
    },
    dateContent :{
      display : 'flex',
      flexDirection : 'row',
    },
    dateChild: {
      position : 'absolute',
      left: 0,
      right : 0,
      top : 'auto',
      bottom : 'auto',
    },
  }));

  export default Background;