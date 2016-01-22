

import { Router } from 'director';
import React, { Component, PropTypes } from 'react';


export default class extends Component {


  static contextTypes = {
    map: PropTypes.object.isRequired,
  };


  /**
   * Listen for map move.
   */
  componentDidMount() {

    this.router = Router({
      '/:x/:y/:z': (x, y, z) => {

        if (this.lock) {
          this.lock = false;
        }

        else {
          this.context.map.setView([y, x], z);
        }

      }
    });

    this.context.map.on('moveend', _.bind(this.onMove, this));

    this.router.init();

  }


  /**
   * Set the route on move.
   */
  onMove() {

    let c = this.context.map.getCenter();
    let z = this.context.map.getZoom();

    var x = c.lng.toFixed(4);
    var y = c.lat.toFixed(4);

    this.lock = true;

    window.history.replaceState(
      undefined,
      undefined,
      `#${x}/${y}/${z}`,
    );

  }


  render() {
    return null;
  }


}
