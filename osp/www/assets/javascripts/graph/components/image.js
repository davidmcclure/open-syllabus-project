

import React, { Component } from 'react';
import L from 'leaflet';
import { findDOMNode } from 'react-dom';

import 'leaflet.Zoomify';


export default class extends Component {


  /**
   * Spin up the leaflet instance.
   */
  componentDidMount() {

    let el = findDOMNode(this.refs.image);

    this.map = L.map(el, {
      zoomControl: false,
    });

    let zoomControl = L.control.zoom({
      position: 'topright',
    });

    this.map.addControl(zoomControl);

  }


  /**
   * Render the image container.
   */
  render() {
    return <div id="image" ref="image"></div>;
  }


}
