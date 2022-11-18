export const state = () => ({
  layersMenu: [],
})

export const mutations = {
  SET_LAYERS_MENU (state, value) {
    state.layersMenu = value
  }
}
