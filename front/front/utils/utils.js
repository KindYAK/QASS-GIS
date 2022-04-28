export function redrawLastLayer(layers) {
  let n = Object.keys(layers)[Object.keys(layers).length - 1]
  layers[n].redraw();
}
