

import _ from 'lodash';
import React, { Component, PropTypes } from 'react';

import config from './fields.yml';


export default class extends Component {


  static contextTypes = {
    map: PropTypes.object.isRequired,
  };


  /**
   * Mount the field boxes.
   */
  componentDidMount() {

    _.each(config, f => {

      let pts = [
        [f.tly, f.tlx],
        [f.tly, f.brx],
        [f.bry, f.brx],
        [f.bry, f.tlx],
        [f.tly, f.tlx],
      ];

      let opts = {
        color: '#ffc600',
        opacity: 1,
        weight: 0.8,
      };

      let box = L.polyline(pts, opts);

      let icon = L.divIcon({
        html: f.label,
        iconSize: null,
      });

      let marker = L.marker([f.bry, f.tlx], { icon });

      this.context.map.addLayer(box);
      this.context.map.addLayer(marker);

    });

  }


  render() {
    return null;
  }


}
