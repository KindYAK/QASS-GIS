export const state = () => ({
  layersMenu: [],
  layersChosen: [],
})

export const getters = {
  layersChosen(state) {
    return state.layersChosen;
  }
}

export const mutations = {
  SET_LAYERS_MENU (state, value) {
    state.layersMenu = value
  },
  SET_LAYERS_CHOSEN (state, value) {
    state.layersChosen = value
  },
}
