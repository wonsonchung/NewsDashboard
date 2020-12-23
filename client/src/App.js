import React, {useEffect, useState} from 'react';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import { createMuiTheme, makeStyles } from '@material-ui/core/styles';
import {useSelector, useDispatch} from 'react-redux'
import './App.css';
import allActions from './actions'
import Album from './component/Album'
import Background from './component/Background';
import Category from './component/Category';
import GridList from './component/GridList';
import {Copyright} from './component/Copyright';
import {NAVER_COLOR, BLUE_COLOR} from './models/colors';
import {DATA} from './component/Data';

const CateButton = ({ classes, dispatch, setCategory, category, buttonName }) => {
  if (buttonName == 'Hot'){
    return (
      <Button className={category === buttonName ? classes.selected : classes.hotButton}
      onClick={()=> {
        dispatch(allActions.categoryActions.setCategory(buttonName));
        setCategory(buttonName);
      }}>{buttonName}</Button>
    );
  } else {
    return (
      <Button className={category === buttonName ? classes.selected : classes.button}
      onClick={()=> {
        dispatch(allActions.categoryActions.setCategory(buttonName));
        setCategory(buttonName);
      }}>{buttonName}</Button>
    );
  }
};

const App = () => {
  const counter = useSelector(state => state.counter)
  const currentUser = useSelector(state => state.currentUser)
  const currentCategory = useSelector(state => state.currentCategory)
  const [category, setCategory] = useState('Hot');
  const dispatch = useDispatch()

  const user = {name: "Rei"}
  const classes = useStyles();
  const datas = DATA;
  
  useEffect(() => {
    dispatch(allActions.userActions.setUser(user))
    dispatch(allActions.categoryActions.setCategory(category))
    let items = [];
    datas.forEach((doc) => {
      const cate = doc.cate;
      const datetime = doc.datetime;
      const title = doc.title;
      if (category == cate) {
        items.push({
          cate: cate,
          datetime: datetime,
          title: title,
        })
      }
    })
  }, [])

  return (
    <div className="App">
      <Background/>
      <React.Fragment>
        <CssBaseline/>
        <main>
          <div className={classes.category}>
            <CateButton classes={classes} dispatch={dispatch} setCategory={setCategory} category={category}
              buttonName={'Hot'}/>
            <CateButton classes={classes} dispatch={dispatch} setCategory={setCategory} category={category}
              buttonName={'정치'}/>
            <CateButton classes={classes} dispatch={dispatch} setCategory={setCategory} category={category}
              buttonName={'경제'}/>
            <CateButton classes={classes} dispatch={dispatch} setCategory={setCategory} category={category}
              buttonName={'사회'}/>
            <CateButton classes={classes} dispatch={dispatch} setCategory={setCategory} category={category}
              buttonName={'생활문화'}/>
            <CateButton classes={classes} dispatch={dispatch} setCategory={setCategory} category={category}
              buttonName={'세계'}/>
            <CateButton classes={classes} dispatch={dispatch} setCategory={setCategory} category={category}
              buttonName={'IT과학'}/>
              <CateButton classes={classes} dispatch={dispatch} setCategory={setCategory} category={category}
                buttonName={'오피니언'}/>
          </div>
        </main>
      </React.Fragment>
      <GridList category={currentCategory.category}/>
      <Copyright/>
      {
        currentUser.loggedIn ? 
        <>
          <h1>Hello, {currentUser.user.name}</h1>
          <h1>Hello, {currentCategory.category}</h1>
          <button onClick={() => dispatch(allActions.categoryActions.setCategory(category))}>Logout</button>
        </> 
        : 
        <>
          <h1>Login</h1>
          <button onClick={() => dispatch(allActions.userActions.setUser(user))}>Login as Rei</button>
        </>
        }
      <h1>Counter: {counter}</h1>
      <button onClick={() => dispatch(allActions.counterActions.increment())}>Increase Counter</button>
      <button onClick={() => dispatch(allActions.counterActions.decrement())}>Decrease Counter</button>
    </div>
  );
}

const useStyles = makeStyles((theme) => ({
  icon: {
    marginRight: theme.spacing(2),
  },
  category: {
    backgroundColor: theme.palette.background.paper,
    fontSize : '10px'
  },
  button: {
    color : 'black',
    fontWeight: 'bolder',
  },
  hotButton: {
    color: "#f50057",
    fontWeight: 'bolder',
  },
  selected: {
    textDecorationLine : 'underline',
    color: NAVER_COLOR,
    fontWeight: 'bolder',
  }
}));

export default App;