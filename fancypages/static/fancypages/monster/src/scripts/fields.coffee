define ['module', 'jquery', 'wysihtml5', 'cs!urlimages'], (module, $, wysihtml5, urlimages) ->

  delay = (ms, func) -> setTimeout func, ms

  class Field
    sync_events: 'change keyup'    

    constructor: (params) ->
      @callbacks = params.callbacks
      @verbose_name = params.verbose_name
      @data_name = params.data_name

    get_value: ->
      @callbacks[0]()

    set_value: (data) ->
      return @callbacks[1](data)

    post_prepare: ->
      if @sync_events      
        @field_node.filter('input').on @sync_events, (event) =>
          @write()

    prepare: ->

    write: ->
      @set_value(@field_node.filter('input').val())

    revert: ->
      if @old_value
        @set_value(@old_value)


  class InputField extends Field
    input_class: 'input-field'

    get_html: ->
      return """
        <label for="dialog-field-#{ @data_name }">#{ @verbose_name }</label>
        <input class="#{ @input_class }" name="dialog-field-#{ @data_name }"></input>
      """

    prepare: ->
      html = @get_html()
      data = @get_value()
      @field_node = $(html)

      if data
        @old_value = data
        @field_node.filter('input').val(data)
      return @field_node      


  class TextField extends InputField
    input_class: 'text-field'

    get_html: ->
      return """
        <label for="dialog-field-#{ @data_name }">#{ @verbose_name }</label>
        <input class="#{ @input_class }" name="dialog-field-#{ @data_name }"></input>
      """

    post_prepare: ->
      super
      @field_node.filter('input').insertOverlay()


  class URLField extends InputField
    input_class: 'url-field'


  class DateField extends Field
    constructor: (params) ->
      super
      @format = params.format

    post_prepare: ->
      if @sync_events
        @field_node.filter('select').on @sync_events, (event) =>
          @write()

    prepare: ->
      now = new Date()
      year = now.getFullYear()
      month = now.getMonth()
      day = now.getDate()

      year_range = [year-10..year+10]      

      month_choices =
        0: 'January'
        1: 'February'
        2: 'March'
        3: 'April'
        4: 'May'
        5: 'June'
        6: 'July'
        7: 'August'
        8: 'September'
        9: 'October'
        10: 'November'
        11: 'December'

      day_range = [1..31]

      html= """
        <label for="dialog-field-#{ @data_name}-year">#{ @verbose_name }</label>
        <select class="year input-small" name="dialog-field-#{ @data_name}-year"></select>
        <select class="month input-small" name="dialog-field-#{ @data_name}-month"></select>
        <select class="day input-small" name="dialog-field-#{ @data_name}-day"></select>                  
      """
      @field_node = $(html)
      @year_select = @field_node.filter('select.year')
      @month_select = @field_node.filter('select.month')
      @day_select = @field_node.filter('select.day')

      for y in year_range
        @year_select.append $("<option value=\"#{ y }\">#{ y }</option>")

      for m, name of month_choices
        @month_select.append $("<option value=\"#{ m }\">#{ name }</option>")

      for d in day_range
        @day_select.append $("<option value=\"#{ d }\">#{ d }</option>")

      data = @get_value()

      if data
        @old_value = data        
        now = new Date(data)     

      @year_select.val(now.getFullYear())
      @month_select.val(now.getMonth())
      @day_select.val(now.getDate())

      return @field_node

    write: ->
      y = @year_select.val()
      m = @month_select.val()
      d = @day_select.val()
      val = $.datepicker.formatDate(@format,  new Date(y, m, d))

      @set_value(val)


  class ImageField extends InputField
    input_class: 'image-field'

    get_html: ->
      return """
        <label for="dialog-field-#{ @data_name }">#{ @verbose_name }</label>
        <input class="#{ @input_class }" name="dialog-field-#{ @data_name }"></input>
      """      

    post_prepare: ->
      super
      conf = module.config()
      @field_node.filter('input').assetPicker
        copyURL: conf.copyHandler      
        assetPath: conf.assetPath
        assetBaseURL: conf.assetBaseURL
        type: 'image'


  class ImageAssetField extends Field
    input_class: 'image-asset-field'

    constructor: (params) ->
      super
      @constraints = params.constraints
      @image_node = params.image_node
      @wrapper = @image_node.parent()
      @image_data = @get_value()
      @cropper = null

    showPreview: (coords) =>
      conf = module.config()

      # Sanity check, some weird DOM changes can cause a crop change and give us dodgy data
      ratio = coords.h / coords.w

      pWidth = @constraints.width[0]
      pHeight = Math.round(pWidth * ratio)

      rounded = 
        x: Math.floor(coords.x)
        y: Math.floor(coords.y)
        x2: Math.floor(coords.x2)
        y2: Math.floor(coords.y2)

      # Save the crop data
      @image_data.params.width = pWidth
      @image_data.params.crop = [rounded.x, rounded.y, rounded.x2, rounded.y2]

      imageBuilder = new urlimages.ImageBuilder(@image_data.partial_url)
      @image_data.final_url =  conf.dynamicAssetBaseURL + imageBuilder.getImage(@image_data.params)

      # Update the preview image
      rx = pWidth / coords.w
      ry = pHeight / coords.h

      @image_data.scaleX = rx
      @image_data.displayWidth = pWidth
      @image_data.displayHeight = pHeight

      @wrapper.css
        width: pWidth + 'px'
        height: pHeight + 'px'

      offsetX = Math.round(rx * rounded.x)
      offsetY = Math.round(ry * rounded.y)

      @image_data.offsetX = offsetX
      @image_data.offsetY = offsetY

      @updatePreview(offsetX, offsetY, rx)

    updatePreview: (offsetX, offsetY, scaleX) =>
      @image_node.css
        marginLeft: '-' + offsetX + 'px'
        marginTop: '-' + offsetY + 'px'

      @image_node.attr('width', Math.round(scaleX * @image_data.width))
      @image_node.attr('height', null)        

    getCropperOptions: ->
      return {
        boxWidth: '355'
        onChange: @showPreview
        onSelect: @showPreview
        minSize: [@constraints.width[0], @constraints.height[0]] 
      }
     
    get_html: ->
      return """
        <div class="image-container">
          <img src="" />
        </div>
      """

    write: ->
      @set_value(@image_data)      

    prepare: ->
      html = @get_html()
      data = @get_value()
      @field_node = $(html)
      @cropper = null

      img = @field_node.find('img')

      if data and not data.placeholder
        @image_data = data
        @old_value = data
        img.attr('src', data.base_url)

        delay 10, =>
          options = @getCropperOptions()
          options.trueSize = [data.width, data.height]
          options.setSelect = [data.params.crop[0], data.params.crop[1], data.params.crop[2], data.params.crop[3]]
          @cropper = $.Jcrop(img, options)
      else
        img.attr('src', @image_node.attr('src'))

        @image_data =
          placeholder: true
          base_url: @image_node.attr('src')
          partial_url: null
          params: null
          width: @image_node.width()
          height: @image_node.height()
          id: null
          final_url: @image_node.attr('src')
      return @field_node

    post_prepare: ->
      super
      conf = module.config()
      @field_node.find('img').assetPicker
        copyURL: conf.copyHandler      
        assetPath: conf.assetPath
        assetBaseURL: conf.assetBaseURL
        type: 'image'
        createTrigger: (elem) =>
          trigger = $('<a class="btn btn-info">Library</a>')
          elem.after(trigger)
          return trigger
        onCopyComplete: (elem, asset, newURL, partialURL) =>
          imageBuilder = new urlimages.ImageBuilder(partialURL)
          @image_data =
            placeholder: false
            base_url: newURL
            partial_url: partialURL
            width: asset.width()
            height: asset.height()
            scaleX: @constraints.width[0] / asset.width()
            params:
              width: @constraints.width[0]
              crop: [0, 0, @constraints.width[0], @constraints.height[0]]
              format: 'jpg'
            id: asset.id()
          
          @image_data.final_url =  conf.dynamicAssetBaseURL + imageBuilder.getImage(@image_data.params)

          elem.attr 'src', newURL
          # We need to make sure the dimensions are correct before initialising the cropper,
          # otherwise it might have warped dimensions :(
          elem.css
            width: asset.width()
            height: asset.height()
          elem.removeClass('asset-target')

          if @cropper
            @cropper.setImage @image_data.base_url, (api) =>
              @cropper.setOptions
                setSelect: [0, 0, asset.width(), asset.height()]
                trueSize: [asset.width(), asset.height()]                 
          else
            options = @getCropperOptions()
            options.setSelect = [0, 0, asset.width(), asset.height()]
            options.trueSize = [asset.width(), asset.height()]               
            @cropper = $.Jcrop(elem, options)
          @write()

  class WYSIWYGField extends Field
    prepare: ->
      html = """
        <label for="dialog-field-#{ @data_name }">#{ @verbose_name }</label>
        <div class="wysihtml5-wrapper">
        <div class="wysihtml5-toolbar" id="dialog-field-toolbar-#{ @data_name }" style="display: none;">
        <ul>
          <li><a class="toolbar-bold" data-wysihtml5-command="bold" title="CTRL+B">bold</a></li>
          <li><a class="toolbar-italic" data-wysihtml5-command="italic" title="CTRL+I">italic</a></li>
          <li><a class="toolbar-link" data-wysihtml5-command="createLink" title="Insert a link" class="command">Add Link</a></li>
          <li><a class="toolbar-insert">Insert</a></li>
          <li><a class="toolbar-unordered" data-wysihtml5-command="insertUnorderedList">Unordered List</a></li>
          <li><a class="toolbar-ordered" data-wysihtml5-command="insertOrderedList">Ordered List</a></li>
          <li><a class="toolbar-break" data-wysihtml5-command="insertLineBreak">Line break</a></li>
          <li><a class="toolbar-html" data-wysihtml5-action="change_view">html view</a></li>
        </ul>
        <div class="data-wysihtml5-dialog" data-wysihtml5-dialog="createLink" style="display: none;">
          <label>Link</label>
          <input data-wysihtml5-dialog-field="href" value="http://">
          <a data-wysihtml5-dialog-action="save" class="btn btn-mini btn-primary">OK</a>&nbsp;<a class="btn btn-mini" data-wysihtml5-dialog-action="cancel">Cancel</a>
        </div>
        </div>
        <textarea class="wysihtml5" name="dialog-field-#{ @data_name }" id="dialog-field-#{ @data_name }"></textarea>
        </div>
      """
      data = @get_value()
      @field_node = $(html)

      if data
        @old_value = data
        @field_node.find('textarea').val(data)
      return @field_node

    post_prepare: ->
      wysihtml5ParserRules =
        tags:
          strong: {}
          b:      {}
          i:      {}
          em:     {}
          br:     {}
          p:      {}
          div:    {}
          span:   {}
          ul:     {}
          ol:     {}
          li:     {}
          a:
            set_attributes:
              rel:    "nofollow"
            check_attributes:
              href:   "url"

      @editor = new wysihtml5.Editor("dialog-field-#{ @data_name }", {
        style: false
        toolbar: "dialog-field-toolbar-#{ @data_name }"
        stylesheets: ['/static/blakey/editor/css/wysihtml5_editor.css']
        parserRules: wysihtml5ParserRules
      })

      @editor.observe "load", () =>
        @editor.composer.element.addEventListener "keyup", () =>
            @write()

      @field_node.filter('textarea').on 'keyup', () =>
        @write()

      @editor.on 'change', (event) =>
        @write()

      @editor.on 'aftercommand:composer', (event) =>
        @write()

      @field_node.find('.toolbar-insert').wysihtml5FieldPicker(@editor)

      @field_node.find('textarea').assetPicker
        type: 'snippet'
        createTrigger: LibraryTriggers.snippetWYSI
        editor: @editor




    write: ->
      @set_value(@editor.getValue())

    revert: ->
      if @old_value
        @set_value(@old_value)



  return {
    Field: Field
    DateField: DateField
    TextField: TextField
    URLField: URLField
    ImageField: ImageField
    ImageAssetField: ImageAssetField
    WYSIWYGField: WYSIWYGField
  }
