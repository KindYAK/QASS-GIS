export function redrawLastLayer(layers) {
  let n = Object.keys(layers)[Object.keys(layers).length - 1]
  layers[n].redraw();
}

export function includesLayer(layers, layer){
  for(let l of layers){
    if (l.layer_name === layer.layer_name) {
      return true;
    }
  }
  return false
}
