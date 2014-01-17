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
    $(".input-workqty").autocomplete({source: [], autoFocus: true, delay: 0})
    $(".input-opus").autocomplete({source: [], autoFocus: true, delay: 0})
    
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

  $("form").on("submit", function(ev) { ev.preventDefault(); console.log("Submit ", $("#search").val()) })

  $("table").stickyTableHeaders()

  $("table").on("change", function(ev) {
    // console.log("Hi")
    // return

    thing = $(ev.target)
    id = thing.attr("id")
    parent = thing.parents("tr")
    music_id = parent.data("music-id")
    console.log(ev, "Field was updated : ", parent, music_id, id)

    thing.css("background-color", "rgb(192, 192, 255)")

    $.post("blarg")
      .done(function() {
        console.log("Done!")
        thing.css("background-color", "")
      })
      .error(function() {
        console.log("There was a problem")
        thing.css("background-color", "rgb(255, 192, 192)")
      })
    // Make a post request
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
