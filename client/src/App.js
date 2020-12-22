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

const App = () => {
  const counter = useSelector(state => state.counter)
  const currentUser = useSelector(state => state.currentUser)
  const currentCategory = useSelector(state => state.currentCategory)
  const dispatch = useDispatch()
  
  const user = {name: "Rei"}
  const classes = useStyles();
  const [category, setCategory] = useState('경제');
  const datas = DATA;

  useEffect(() => {
    dispatch(allActions.userActions.setUser(user))
    dispatch(allActions.categoryActions.setCategory(category))
    let items = [];
    datas.forEach((doc) => {
      const cate = doc.cate;
      const datetime = doc.datetime;
      const title = doc.title;
      if ((category == cate)) {
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
            <Button className={category === 'Hot' ? classes.selected : classes.hotButton}
              onClick={()=> {
                dispatch(allActions.categoryActions.setCategory('Hot'));
                setCategory('Hot');
              }}>Hot</Button>
            <Button className={category === '정치' ? classes.selected : classes.button}
              onClick={()=> {
                dispatch(allActions.categoryActions.setCategory('정치'));
                setCategory('정치');
              }}>정치</Button>
            <Button className={category === '경제' ? classes.selected : classes.button}
              onClick={()=> {
                dispatch(allActions.categoryActions.setCategory('경제'));
                setCategory('경제');
              }}>경제</Button>
            <Button className={category === '사회' ? classes.selected : classes.button}
              onClick={()=> {
                dispatch(allActions.categoryActions.setCategory('사회'));
                setCategory('사회');
              }}>사회</Button>
            <Button className={category === '생활문화' ? classes.selected : classes.button}
              onClick={()=> {
                dispatch(allActions.categoryActions.setCategory('생활문화'));
                setCategory('생활문화');
              }}>생활문화</Button>
            <Button className={category === '세계' ? classes.selected : classes.button}
              onClick={()=> {dispatch(allActions.categoryActions.setCategory('세계'));
                setCategory('세계');
              }}>세계</Button>
            <Button className={category === 'IT과학' ? classes.selected : classes.button}
              onClick={()=> {
                dispatch(allActions.categoryActions.setCategory('IT과학'));
                setCategory('IT과학');
              }}>IT과학</Button>
            <Button className={category === '오피니언' ? classes.selected : classes.button}
              onClick={()=> {dispatch(allActions.categoryActions.setCategory('오피니언'));
              setCategory('오피니언');
            }}>오피니언</Button>
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