export function redrawLastLayer(layers) {
  for(let i = 0; i <= 5; i++) {
    try {
      let n = Object.keys(layers)[Object.keys(layers).length - 1]
      layers[n].redraw();
    } catch {
      continue
    }
    break
  }
}

export function includesLayer(layers, layer){
  for(let l of layers){
    if (l.layer_name === layer.layer_name) {
      return true;
    }
  }
  return false
}
