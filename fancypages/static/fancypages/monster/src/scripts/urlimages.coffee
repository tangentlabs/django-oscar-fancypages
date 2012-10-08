define ['module'], (module) ->

  class ImageBuilder
    constructor: (@baseImageURL) ->
      extIndex = @baseImageURL.lastIndexOf('.') 
      @ext = @baseImageURL[extIndex..]

    getImage: (params) ->
      extChanged = false
      bits = []

      for key, value of params
        if key == 'format'
          ext = value
          extChanged = true
        else if key == 'crop'
          joined = value.join(',')
          bits.push("#{ key }-#{ joined }")
        else
          bits.push("#{ key }-#{ value }")

      if bits
        suffix = bits.join('_')
        path = [@baseImageURL, suffix, ext].join('.')
      else
        if extChanged
            path = [@baseImageURL, 'to', ext].join('.')
      return path

  return {
    ImageBuilder: ImageBuilder
  }