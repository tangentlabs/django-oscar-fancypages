define ['jquery', 'cs!fields'], ($, fields) ->
  class Widget
    constructor: (@editor, @node, @data) ->
      @clean_html = @node.outerHTML()

    get_data: ->
      @node.html()

    render: ->
      @node.outerHTML()


  class Container extends Widget
    constructor: (@editor, @node, @data) ->
      super

      @block_options = []
      @block_options_by_type = {}

      @node.widgets().filter(@container_nodes).each(@build_options)
      @node.empty()

      if @data
        for val in @data
          temp = $(@block_options_by_type[val.type])
          @node.append(temp)
          @editor.editor_for_node(temp, val.data)
      else
        temp = $(@block_options[0].html)
        @node.append(temp)
        @editor.editor_for_node(temp, null)

      select = $('<select style="float: left">')

      for temp, i in @block_options
        option = $('<option>')
        option.attr('value', i)
        option.text(temp.label)
        select.append(option)

      handler = $("""
        <div class="ui-widget-header ui-helper-clearfix ui-corner-all" style="z-index: 9999; margin: 0 0 10px; padding: 2px;">
          <span class="add ui-corner-all">
            <span class="ui-icon ui-icon-plus"></span>
          </span>
        </div>""")
      handler.prepend(select)
      @node.append(handler)

      @node.sortable
        handle: 'span.move'
        scroll: true
        tolerance: 'pointer'
        items: ':widget'
        forcePlaceholderSize: true
        placeholder: 'sortable-placeholder'

      handler.on 'click', 'span.add', (event) =>
        event.preventDefault()
        new_node = $(@block_options[select.get(0).value].html)
        new_node.data 'widget', new Block(@editor, new_node, null)
        new_node.hide()
        $(event.target).closest('.ui-widget-header').before(new_node)
        new_node.fadeIn(400)

    get_data: ->
      $.map @node.widgets(), (elem, i) =>
        @editor.data_for_node $(elem)

    render: ->
      container = $(@clean_html).empty()

      @node.widgets().each (i, elem) =>
        container.append(@editor.render_node($(elem)))

      return container or null

    build_options: (i, elem) =>
      $elem = $(elem)

      html = $('<div />').append($elem.clone()).remove().html()
      label = $elem.attr('m:label')

      @block_options_by_type[label] = html

      @block_options[i] =
        label: label
        html: html

    container_nodes: (elem) ->
      $(elem).attr('m_widget') isnt 'container'


  class Block extends Widget
    constructor: (@editor, @node, @data) ->
      super
      temp = @node.widgets()

      temp.each (i, elem) =>
        @editor.editor_for_node $(elem), if @data then @data[i] else null

      handler = $("""
        <div class="ui-widget-header ui-helper-clearfix ui-corner-all" style="z-index: 9999; position: absolute; top: -2px; right: -2px; width: 32px; height: 16px; padding: 2px;">
          <span class="move ui-corner-all">
            <span style="position: absolute; left: 1; top: 1;" class="ui-icon ui-icon-arrow-4">Move</span>
          </span>
          <span class="delete ui-corner-all">
            <span style="position: absolute; left: 17px; top: 1;" class="ui-icon ui-icon-trash">Remove</span>
          </span>
        </div>
      """)
      @node.prepend(handler)
      @node.css
        position: 'relative'

      handler.hide()

      @node.on 'hover', (event) =>
        if event.type is 'mouseenter'
          handler.show()
        else
          handler.hide()

      @node.on 'click', (event) =>
        event.preventDefault()
        event.stopPropagation()

      handler.on 'click', 'span.delete', (event) =>
        event.preventDefault()
        @node.fadeOut 400, =>
          @node.remove()

    get_data: ->
      temp = @node.widgets()
      result =
        type: @node.attr('m:label')
        data: []

      temp.each (i, elem) =>
        result['data'].push(@editor.data_for_node($(elem)))

      return result

    render: ->
      duplicate = $(@clean_html)
      @node.widgets().each (i, elem) =>
        html = @editor.render_node($(elem))
        duplicate.widgets().eq(i).replaceWith(html)

      return duplicate


  class EditableGroup extends Widget
    constructor: (@editor, @node, @data) ->
      super
      @widgets = @node.widgets()

      @widgets.each (i, elem) =>
        @editor.editor_for_node $(elem), if @data then @data[i] else null

      edit_button = $('<span class="edit-button">Edit</span>')

      @node.before(edit_button)

      edit_button.on 'click', (event) =>
        event.preventDefault()
        event.stopPropagation()

        html = $('''
          <div class="scrollpane">
            <div class="scrollparent">
              <div class="scrollchild">
              </div>
            </div>
          </div>
        ''')

        pane = html.find('.scrollchild')

        @widgets.each (i, elem) =>
          label = $(elem).attr('m:label')

          container = $("""
            <div class="widget-settings">
              <div class="widget-heading">#{ label }</div>
            </div>
          """)
          $(elem).data('widget').prepare(container)
          pane.append(container)

        @buttons = $('''
          <div class="buttons">
            <a class="btn cancel">Cancel</a>
            <a class="btn btn-success save">Keep Changes</a>
          </div>
        ''')

        $('.editor .controls').append(html)
        @controls = $('.editor .controls')

        @controls.empty()
        @controls.append html
        @controls.append @buttons
        @post_prepare()

        @buttons.on 'click', 'a.save', (event) =>
          @write()
          @controls.empty()
        @buttons.on 'click', 'a.cancel', (event) =>
          @revert()
          @controls.empty()

    write: ->
      @widgets.each (i, elem) =>
        $(elem).data('widget').write()

    revert: ->
      @widgets.each (i, elem) =>
        $(elem).data('widget').revert()

    post_prepare: ->
      @widgets.each (i, elem) =>
        $(elem).data('widget').post_prepare()

      # Scrollbar and footer docking behaviour
      enabled = false
      adjustSidebar = () =>

        $('.scrollparent').css
          height: 'auto'

        parentHeight = $('.scrollparent').height()
        childHeight = $('.scrollchild').height()

        if childHeight > parentHeight
          if not enabled
            enabled = true
            #$('.scrollpane').nanoScroller
            #  preventPageScrolling: true
          @buttons.css
            bottom: '0'
            top: 'auto'
          $('.scrollparent').css
            height: 'auto'
            'overflow-y': 'scroll'
        else
          if enabled
            enabled = false
            #$(".nano").nanoScroller
            #  stop: true
          @buttons.css
            bottom: 'auto',
            top: $('.scrollchild').outerHeight() + 'px'
          $('.scrollparent').css
            height: childHeight
            'overflow-y': 'hidden'

      #$(".scrollpane").nanoScroller
      #  contentClass: 'scrollparent'

        stop: true
      adjustSidebar()

      $(window).on 'resize', adjustSidebar


    get_data: ->
      result = []
      @widgets.each (i, elem) =>
        result.push @editor.data_for_node($(elem))

      return result

    render: ->
      duplicate = $(@clean_html)
      @widgets.each (i, elem) =>
        html = @editor.render_node($(elem))
        duplicate.widgets().eq(i).replaceWith(html)

      return duplicate


  class DialogWidget extends Widget
    title: 'Dialog'

    init_fields: ->
      @fields = {}

    constructor: (@editor, @node, @data) ->
      super
      @init_fields()

      # edit_button = $('<span class="edit-button">Edit</span>')

      # @node.before(edit_button)

      # edit_button.on 'click', (event) =>
      #   event.preventDefault()
      #   event.stopPropagation()

      #   container = $('''
      #             <div class="widget-settings">
      #             </div>
      #           ''')
      #   @prepare(container)

      #   container.append('''
      #             <div class="buttons">
      #               <a class="btn cancel">Cancel</a>
      #               <a class="btn btn-success save">Keep Changes</a>
      #             </div>
      #           ''')

      #   controls = $('.editor .controls')

      #   existing = controls.find '.widget-settings'

      #   deferred = false

      #   add_new = () =>
      #     container.hide()
      #     controls.empty()
      #     controls.append container
      #     container.slideDown 100, () =>
      #       @post_prepare(container)

      #   if existing.length > 0
      #     deferred = true
      #     wait = existing.fadeOut 200, () =>
      #       add_new()

      #   if not deferred
      #     add_new()

      #   container.on 'click', 'a.save', (event) =>
      #     @write()
      #     container.remove()
      #   container.on 'click', 'a.cancel', (event) =>
      #     @revert()
      #     container.remove()

      @init()

    prepare: (container) ->
      for name, field of @fields
        field_node = field.prepare()
        field_node_wrapped = $('<div class="field" />').append(field_node)
        container.append(field_node_wrapped)

    post_prepare: ->
      for name, field of @fields
        field.post_prepare()

    init: ->
      if @data
        for name, field of @fields
          field.set_value(@data[field.data_name])

    write: ->
      for name, field of @fields
          field.write()

    revert: ->
      for name, field of @fields
          field.revert()

    get_title: ->
      return @title

    get_data: ->
      result = {}
      for name, field of @fields
        result[field.data_name] = field.get_value()
      return result


  class LinkedHeading extends DialogWidget
    title: 'Linked Heading'

    init_fields: ->
      @fields =
        text: new fields.TextField
          verbose_name: "Text"
          callbacks: [
            => @node.find('a').html()
            (data) => @node.find('a').html(data)
          ]
          data_name: "text"
        href: new fields.URLField
          verbose_name: "Link URL"
          callbacks: [
            => @node.find('a').attr('href')
            (data) => @node.find('a').attr('href', data)
          ]
          data_name: 'href'
        title: new fields.TextField
          verbose_name: "Link Title"
          callbacks: [
            => @node.find('a').attr("title")
            (data) => @node.find('a').attr('title', data)
          ]
          data_name: "title"



  class LinkedImage extends DialogWidget
    title: 'Linked Image'

    init_fields: ->
      @fields =
        src: new fields.ImageField
          verbose_name: "URL"
          callbacks: [
            => @node.find('img').attr('src')
            (data) =>
              @node.find('img').attr('src', data)
          ]
          data_name: "src"
        alt: new fields.TextField
          verbose_name: "Alt Text"
          callbacks: [
            =>
              @node.find('img').attr('alt')
            (data) =>
              @node.find('img').attr('alt', data)
          ]
          data_name: 'alt'
        href: new fields.URLField
          verbose_name: "Link URL"
          callbacks: [
            => @node.attr('href')
            (data) => @node.attr('href', data)
          ]
          data_name: 'href'
        title: new fields.TextField
          verbose_name: "Link Title"
          callbacks: [
            => @node.attr("title")
            (data) => @node.attr('title', data)
          ]
          data_name: "title"


  class LinkedImageAsset extends DialogWidget
    title: "Linked Image"

    render: ->
      @image_node.unwrap()

      if @image_data and not @image_data.placeholder
        @image_node.attr('src', @image_data.final_url)
        @image_node.css
          marginLeft: 'auto'
          marginTop: 'auto'
        @image_node.attr('width', @image_data.params.width)
        @image_node.attr('height', null)
      super

    init_fields: ->
      @width = @node.data('width')
      @height = @node.data('height')

      if not @width
        @maxWidth = @node.data('max-width')
        @minWidth = @node.data('min-width')
      else
        @maxWidth = @minWidth = @width

      if not @height
        @maxHeight = @node.data('max-height')
        @minHeight = @node.data('min-height')
      else
        @maxHeight = @minHeight = @height

      @image_node = @node.find('img')
      @image_node.wrap """<div style="overflow: hidden;" />"""
      @wrapper = @image_node.parent()

      if not @data
        @data =
          image:
            placeholder: true
            base_url: @image_node.attr('src')
            partial_url: null
            params: null
            width: @image_node.width()
            height: @image_node.height()
            id: null
            final_url: @image_node.attr('src')

      if @data and @data.image.placeholder
        scaleX = @data.image.scaleX
        offsetX = @data.image.offsetX
        offsetY = @data.image.offsetY

        @wrapper.css
          width: @data.image.displayWidth + 'px'
          height: @data.image.displayHeight + 'px'

        @image_node.css
          marginLeft: '-' + offsetX + 'px'
          marginTop: '-' + offsetY + 'px'
        @image_node.attr('width', Math.round(scaleX * @data.image.width))
        @image_node.attr('height', null)

      @fields =
        image: new fields.ImageAssetField
          image_node: @image_node
          image_data: @image_data
          constraints:
            width: [@minWidth, @maxWidth]
            height: [@minHeight, @maxHeight]
          verbose_name: "Image"
          callbacks: [
            => @image_data
            (data) =>
              @image_data = data
              @node.find('img').attr('src', @image_data.base_url)
          ]
          data_name: 'image'
        alt: new fields.TextField
          verbose_name: "Alt Text"
          callbacks: [
            =>
              @node.find('img').attr('alt')
            (data) =>
              @node.find('img').attr('alt', data)
          ]
          data_name: 'alt'
        href: new fields.URLField
          verbose_name: "Link URL"
          callbacks: [
            => @node.attr('href')
            (data) => @node.attr('href', data)
          ]
          data_name: 'href'
        title: new fields.TextField
          verbose_name: "Link Title"
          callbacks: [
            => @node.attr("title")
            (data) => @node.attr('title', data)
          ]
          data_name: "title"


  class Line extends DialogWidget
    title: 'Line'

    init_fields: ->
      @fields =
        text: new fields.TextField
          verbose_name: "Text"
          callbacks: [
            => @node.text()
            (data) => @node.text(data)
          ]
          data_name: "text"


  class DateWidget extends DialogWidget
    title: 'Date'

    init_fields: ->
      @fields =
        date: new fields.DateField
          verbose_name: "Date"
          callbacks: [
            => @node.text()
            (data) => @node.text(data)
          ]
          data_name: "date"
          format: @node.attr('m:format')


  class WYSIWYG extends DialogWidget
    title: 'Rich Text'

    init_fields: ->
      @fields =
        text: new fields.WYSIWYGField
          verbose_name: "Rich Text"
          callbacks: [
            => @node.html()
            (data) => @node.html(data)
          ]
          data_name: "rich_text"


  return {
    Container: Container
    Block: Block
    Date: DateWidget
    EditableGroup: EditableGroup
    DialogWidget: DialogWidget
    LinkedHeading: LinkedHeading
    LinkedImage: LinkedImage
    LinkedImageAsset: LinkedImageAsset
    Line: Line
    WYSIWYG: WYSIWYG
  }