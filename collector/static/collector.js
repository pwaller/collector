$(function() {
  // $(".input-musictype")
  //   .autocomplete({
  //     source: ["hi", "hallo", "hello"],
  //     autoFocus: true,
  //     select: function(ev, ui) {
  //       $(this).blur()
  //     }
  //   })

  if (have_autocomplete) {
    $(".input-composer").autocomplete({source: composers, autoFocus: true, delay: 0})
    $(".input-musictype").autocomplete({source: music_types, autoFocus: true, delay: 0})
    $(".input-keys").autocomplete({source: keys, autoFocus: true, delay: 0})
    $(".input-instrument").autocomplete({source: instruments, autoFocus: true, delay: 0})
    $(".input-conductor").autocomplete({source: conductors, autoFocus: true, delay: 0})
    $(".input-soloists").autocomplete({source: soloists, autoFocus: true, delay: 0})
    $(".input-chorus").autocomplete({source: choruses, autoFocus: true, delay: 0})
    $(".input-ensemble").autocomplete({source: ensembles, autoFocus: true, delay: 0})
    $(".input-music-class").autocomplete({source: musicClasses, autoFocus: true, delay: 0})

    $(".inputable").autocomplete({source: []})

    $(".input-title").on("focusin", function() {
      // console.log("Focussed: ", $(this))
      // foo = $(this);
      var theButton = $(this).parents("tr").find("button")
      theButton.animate({opacity: "toggle"})
    })
    $(".input-title").on("focusout", function() {
      console.log("unFocussed: ", $(this))
      var theButton = $(this).parents("tr").find("button")
      theButton.animate({opacity: "toggle"})
      // setTimeout(function() {
      //   theButton.hide()
      // }, 1000);
    })


    $("table").on("focusin", function() {

    })
    // $(".input-workqty").autocomplete({source: [], autoFocus: true, delay: 0})
    // $(".input-opus").autocomplete({source: [], autoFocus: true, delay: 0})
    
  }

  $("#search")
    .autocomplete({
      source: "/query",
      minLength: 1,
      delay: 50,
      // source: function(request, response) {
      //   //[ "c++", "java", "php", "coldfusion", "javascript", "asp", "ruby" ],

      //   $.getJSON("/query", {"q": request.term})
      //     .done(function(data) {
      //       console.log("Got data back: ", data)
      //       response(data)
      //     })
      //     .fail(function() { response([]) })
      // },
      autoFocus: true,
      select: function(ev, ui) {
        $(this).val(ui.item.music_id)
        window.location = (
          "/covers/" + ui.item.cover_id + "#{\"music_id\":" + ui.item.music_id + "}")
        // $(this).val()
        // $("#search").val()
        // $("#search")
        // console.log("Value was chosen.. ", ui.item.value, ui)
        return false;
      }
    })
    .on("input", function() {
      console.log("Hi", $(this).val())
    })
    .on("autocompleteselect", function() {
      console.log("Chosen.. ", $(this).val())
    })

  // TODO: conditional on whether #search is present?

  if ($("#search").length > 0) {
    $("#search")
      .data("ui-autocomplete")._renderItem = function(ul, item) {
        return $("<li>")
          .append("<a>" + item.attr + '<br><small style="color: #999">' + item.cover_title + "</small></a>")
          .appendTo(ul);
      };
  }

  // $(".form-search").on("submit", function(ev) { ev.preventDefault(); console.log("Submit ", $("#search").val()) })

  // $("#newCoverForm").on("submit", function(ev) {

  // })

  $(".sticky-header").stickyTableHeaders()

  var animateInProgress = function(what) {
    what.animate({"background-color": "#eaeaff"}, 100);
  }

  var animateSuccess = function(what) {
    thing.animate({"background-color": "#aaffaa"}, 200)
         .animate({"background-color": "transparent"}, 1500)
  }

  var animateFailure = function(what) {
    thing.animate({"background-color": "#ffaaaa"}, 200)
  }

  $("#cover-title").on("change", function(ev) {

    thing = $(this);

    cover_id = thing.data("cover-id")
    value = thing.text()

    animateInProgress(thing)

    $.ajax({type: "put", dataType: "json", data: {cover_id: cover_id, field: "title", value: value }})
      .done(function() {
        animateSuccess(thing)
      })
      .error(function() {
        animateFailure(thing)
      })
  })


  $("#cover-notes").on("change", function(ev) {

    thing = $(this);

    cover_id = thing.data("cover-id")
    value = thing.val() // NOTE: this line is different between things

    animateInProgress(thing)

    // return

    $.ajax({type: "put", dataType: "json", data: {cover_id: cover_id, field: "notes", value: value }})
      .done(function() {
        animateSuccess(thing)
      })
      .error(function() {
        animateFailure(thing)
      })
  })

  $(".table-editable").on('focus', "div", function() {
    console.log("Focus")
    contentBefore = $(this).html();
  }).on('blur', "div", function() { 
    console.log("Blur")
    if (contentBefore != $(this).html()) {
      console.log("CHANGED!")
      $(this).trigger('change')
    }
  })

  // TODO(pwaller): change isn't taking for new rows added, may be I need something better than "on"?
  $(".table-editable").on("change", "div", function(ev) {
    // console.log("Hi")
    // return

    thing = $(ev.target)
    field = thing.attr("id")
    parent = thing.parents("tr")
    music_id = parent.data("music-id")
    value = thing.text()
    console.log("Field was updated : ", music_id, field, value)

    animateInProgress(thing)

    $.ajax({type: "put", dataType: "json", data: {music_id: music_id, field: field, value: value }})
      .done(function() {
        animateSuccess(thing)
      })
     .error(function() {
        animateFailure(thing)
      })
    // Make a post request
  })

  // $("#add-row").focus()

  $("#add-row").click(function() {

    row = $(this).parents("tr")

    second = row.prev()
    first = second.prev()

    first = first.clone(); first.find("div").html("");
    second = second.clone(); second.find("div").html("");

    first.toggleClass("tr-even")
    second.toggleClass("tr-even")

    first.removeClass("hide-row")
    second.removeClass("hide-row")

    console.log("First ", first)
    console.log("Second ", second)

    first.find("div").first().focus()

    row.before(first).before(second)
    // TODO: toggle 'tr-even'-ness
    row.toggleClass("tr-even")

    $.ajax({type: "post", dataType: "json", data: {}})
      .done(function() {
        console.log("New music requested")
      })
      .error(function() {
        console.log("There was a problem")
      })
  })

  $("#search").focus()

  try {
    var hash_obj = JSON.parse(window.location.hash.substring(1))
    console.log("music id = ", hash_obj.music_id)
    var music_id = hash_obj.music_id
    $("[data-music-id=" + music_id + "]").addClass("warning")

    // TODO: Pin the exception to SyntaxError
  } catch (e) {
    console.log("Blah: ", e)
  }
})
