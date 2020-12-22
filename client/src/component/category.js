// import React, { useEffect, useState } from 'react';
// import AppBar from '@material-ui/core/AppBar';
// import Button from '@material-ui/core/Button';
// import LibraryBooksIcon from '@material-ui/icons/LibraryBooks';
// import Card from '@material-ui/core/Card';
// import CardActions from '@material-ui/core/CardActions';
// import CardContent from '@material-ui/core/CardContent';
// import CardMedia from '@material-ui/core/CardMedia';
// import CssBaseline from '@material-ui/core/CssBaseline';
// import Grid from '@material-ui/core/Grid';
// import Toolbar from '@material-ui/core/Toolbar';
// import Typography from '@material-ui/core/Typography';
// import { createMuiTheme, makeStyles } from '@material-ui/core/styles';
// import Container from '@material-ui/core/Container';
// import Link from '@material-ui/core/Link';
// import {NAVER_COLOR, BLUE_COLOR} from '../models/colors';
// import {DATA} from './Data';

// function Category({data}) {
//   const classes = useStyles();
//   const [category, setCategory] = useState('Hot');
//   const datas = DATA;

//   useEffect(() => {
//     let items = [];
//     datas.forEach((doc) => {
//       const cate = doc.cate;
//       const datetime = doc.datetime;
//       const title = doc.title;
//       if ((category == cate)) {
//         items.push({
//           cate: cate,
//           datetime: datetime,
//           title: title,
//         })
//       }
//     })
//   });

//   return (
//     <React.Fragment>
//         <CssBaseline/>
//         <main>
//           <div className={classes.category}>
//             <Button className={category === 'Hot' ? classes.selected : classes.hotButton}
//               onClick={()=> {setCategory('Hot')}}
//               >Hot</Button>
//             <Button className={category === '정치' ? classes.selected : classes.button}
//               onClick={()=> {setCategory('정치')}}>정치</Button>
//             <Button className={category === '경제' ? classes.selected : classes.button}
//               onClick={()=> {setCategory('경제')}}>경제</Button>
//             <Button className={category === '사회' ? classes.selected : classes.button}
//               onClick={()=> {setCategory('사회')}}>사회</Button>
//             <Button className={category === '생활문화' ? classes.selected : classes.button}
//               onClick={()=> {setCategory('생활문화')}}>생활문화</Button>
//             <Button className={category === '세계' ? classes.selected : classes.button}
//               onClick={()=> {setCategory('세계')}}>세계</Button>
//             <Button className={category === 'IT과학' ? classes.selected : classes.button}
//               onClick={()=> {setCategory('IT과학')}}>IT과학</Button>
//             <Button className={category === '오피니언' ? classes.selected : classes.button}
//               onClick={()=> {setCategory('오피니언')}}>오피니언</Button>
//           </div>
//         </main>
//     </React.Fragment>
//   );
// }

// const useStyles = makeStyles((theme) => ({
//   icon: {
//     marginRight: theme.spacing(2),
//   },
//   category: {
//     backgroundColor: theme.palette.background.paper,
//   },
//   button: {
//     color : 'black',
//     fontWeight: 'bolder',
//   },
//   hotButton: {
//     color: "#f50057",
//     fontWeight: 'bolder',
//   },
//   selected: {
//     textDecorationLine : 'underline',
//     color: NAVER_COLOR,
//     fontWeight: 'bolder',
//   }
// }));


// export default Category;