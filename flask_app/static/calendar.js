$(function () {
   var today = new Date(),
   tomorrow = new Date(new Date().getTime() + 24 * 60 * 60 * 1000);

   $("#currentTime").igDateEditor({
      dateInputFormat: "dateTime",
      value: new Date(),
      dataMode: "date",
      readOnly: true
   });

   $("#outboundpartialdate").igDatePicker({
      dateInputFormat: "yyyy-MM-dd",
      value: today,
      regional: "en-US",
      dataMode: "date",
      datepickerOptions: {
            minDate: today
               },
      valueChanged: function (evt, ui) {
            if (ui.newValue instanceof Date) {
               var nextDay = new Date(ui.newValue.getTime() + 24 * 60 * 60 * 1000);
               var currentValue = $("#returndate").igDatePicker("option", "value");
               if (currentValue.getTime() > nextDay.getTime()) {
                  $("#returndate").igDatePicker("option", "datepickerOptions", {
                        minDate: nextDay
                  }).igDatePicker("option", "value", nextDay)
               } else {
                  $("#returndate").igDatePicker("option", "value", nextDay).igDatePicker("option", "datepickerOptions", {
                        minDate: nextDay
                  })
               }
            }
         }
   });
   $("#returndate").igDatePicker({
      value: tomorrow,
      dateInputFormat: "yyyy-MM-dd",
      regional: "en-US",
      dataMode: "date",
      datepickerOptions: {
         minDate: tomorrow,
         numberOfMonths: [1, 2]
      }
   });
});

var options = {
   shouldSort: true,
   threshold: 0.4,
   maxPatternLength: 32,
   keys: [{
      name: 'iata',
      weight: 0.5
   }, {
      name: 'name',
      weight: 0.3
   }, {
      name: 'city',
      weight: 0.2
   }]
};

var fuse = new Fuse(airports, options)

var ac = $('#searchairport')
.on('click', function(e) {
   e.stopPropagation();
})
.on('focus keyup', search)
.on('keydown', onKeyDown);

var wrap = $('<div>')
.addClass('autocomplete-wrapper')
.insertBefore(ac)
.append(ac);

var list = $('<div>')
.addClass('autocomplete-results')
.on('click', '.autocomplete-result', function(e) {
   e.preventDefault();
   e.stopPropagation();
   selectIndex($(this).data('index'));
})
.appendTo(wrap);

$(document)
.on('mouseover', '.autocomplete-result', function(e) {
   var index = parseInt($(this).data('index'), 10);
   if (!isNaN(index)) {
   list.attr('data-highlight', index);
   }
})
.on('click', clearResults);

function clearResults() {
   results = [];
   numResults = 0;
   list.empty();
}

function selectIndex(index) {
   if (results.length >= index + 1) {
      ac.val(results[index].iata);
      clearResults();
   }  
}

var results = [];
var numResults = 0;
var selectedIndex = -1;

   

function search(e) {
   if (e.which === 38 || e.which === 13 || e.which === 40) {
      return;
   }
    
   if (ac.val().length > 0) {
      results = _.take(fuse.search(ac.val()), 7);
      numResults = results.length;
        
      var divs = results.map(function(r, i) {
         return '<div class="autocomplete-result" data-index="'+ i +'">'
               + '<div><b>'+ r.iata +'</b> - '+ r.name +'</div>'
               + '<div class="autocomplete-location">'+ r.city +', '+ r.country +'</div>'
               + '</div>';
      });
      
      selectedIndex = -1;
      list.html(divs.join(''))
      .attr('data-highlight', selectedIndex);

   } else {
      numResults = 0;
      list.empty();
   }
}

function onKeyDown(e) {
   switch(e.which) {
      case 38: // up
      selectedIndex--;
      if (selectedIndex <= -1) {
         selectedIndex = -1;
      }
      list.attr('data-highlight', selectedIndex);
      break;
      case 13: // enter
      selectIndex(selectedIndex);
      break;
      case 9: // enter
      selectIndex(selectedIndex);
      e.stopPropagation();
      return;
      case 40: // down
      selectedIndex++;
      if (selectedIndex >= numResults) {
         selectedIndex = numResults-1;
      }
      list.attr('data-highlight', selectedIndex);
      break;

      default: return; // exit this handler for other keys
   }
   e.stopPropagation();
   e.preventDefault(); // prevent the default action (scroll / move caret)

}