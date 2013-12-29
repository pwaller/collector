$(function() {
  console.log("Hello world")

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
