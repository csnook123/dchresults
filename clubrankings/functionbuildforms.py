


def dropdown(event_list):
  dd = '<h6>Number of Performances by year</h1>'
  dd += '<form action="/action_page.php">'
  dd +='<label for="events">Choose an Event:</label>'
  dd +=  '<select name="events" id="events">'
  for str in event_list:
    dd +=    '<option value="' + str + '" color: black >' +str +'</option>'
  dd += '</select>'
  return dd
  