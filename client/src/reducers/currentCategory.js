const currentCategory = (state = {}, action) => {
    switch(action.type){
        case "SET_CATEGORY":
            return {
                ...state,
                category: action.category,
            }
        default:
            return state
    }
}

export default currentCategory;