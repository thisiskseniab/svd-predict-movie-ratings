var graph = new Rickshaw.Graph( {
          element: document.querySelector("#chart"),
          width: 250,
          height: 150,
          renderer: 'bar',
          series: [ 
            {
              data: [ { x: 0, y: 40 }, { x: 1, y: 49 }, { x: 2, y: 38 }, { x: 3, y: 30 }, { x: 4, y: 32 } ],
              color: '#4682b4'
            }, {
              data: [ { x: 0, y: 20 }, { x: 1, y: 24 }, { x: 2, y: 19 }, { x: 3, y: 15 }, { x: 4, y: 16 } ],
              color: '#9cc1e0'

          }, {
           data: [ { x: 0, y: 5 }, { x: 1, y: 8 }, { x: 2, y: 6 }, { x: 3, y: 10 }, { x: 4, y: 7 } ],
              color: '#BDC3C7'

          } ]
        } );
        graph.render();

var graph = new Rickshaw.Graph( {
          element: document.querySelector("#chart2"),
          width: 250,
          height: 150,
          renderer: 'line',
          series: [ 
            {
              data: [ { x: 0, y: 40 }, { x: 1, y: 49 }, { x: 2, y: 38 }, { x: 3, y: 30 }, { x: 4, y: 32 } ],
              color: '#4682b4'
            }, {
              data: [ { x: 0, y: 20 }, { x: 1, y: 24 }, { x: 2, y: 19 }, { x: 3, y: 15 }, { x: 4, y: 16 } ],
              color: '#9cc1e0'

          } ]
        } );
        graph.render();