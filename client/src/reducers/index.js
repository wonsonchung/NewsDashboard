import currentUser from './currentUser'
import counter from './counter'
import currentCategory from './currentCategory'

import {combineReducers} from 'redux'

const rootReducer = combineReducers({
    currentUser,
    counter,
    currentCategory
})

export default rootReducer