function showDiv(data) {
    $("#ele-" + data).show();
    hideElement(exit_integer, data);
  }

  function hideElement(total, active) {
    for (i = 0; i <= total; i++) {
      if (i != active)
        $("#ele-" + i).hide();
    }
  }

  function hideAnswers(total, active) {
    for (i = 0; i <= total; i++) {
      if (i != active)
        $("#card-answer-" + i).hide();
    }
    $("div[id*='card-answer']").each(function (i, el) {
         $('#'+el.id).hide()
     });
  }

  $(document).ready(function(){
    showDiv(counter);
});

var dict, exit_integer;
window.addEventListener("load", function(){
  dict = {"deck_id": $('#deck-id').text()}
  exit_integer = parseInt(
    $("#exit-integer").text()
  )
  console.log(exit_integer)
});

var counter = 0
var shown = false
document.addEventListener("keypress", function onPress(event) {
  console.log(counter)
  if (event.key === "z") {
      id = $("#card-id-" + counter).text()
      counter++;
      dict[counter] = {id: id, result: 'z'}
      console.log(dict);
      $('#card-answer-' + counter).hide();
      showDiv(counter);
  } else if (event.key === "x") {
      id = $("#card-id-" + counter).text()
      counter++;
      dict[counter] = {id: id, result: 'x'}
      console.log(dict);
      $('#card-answer-'+counter).hide();
      showDiv(counter);
  } else if (event.key === "s") {
      $('#card-answer-'+counter).show()
  }
  if (counter === exit_integer) {
    fetch(
      $('#redirect-url').text(), {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dict)
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
    })
    .catch(function(err) {
        console.info(err + " url: " + url);
    });
  }
});



window.onbeforeunload = function() {
  fetch(
    $('#redirect-url').text(), {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dict)
    })
return;
}
