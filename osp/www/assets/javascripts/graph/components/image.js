

import React, { Component } from 'react';
import L from 'leaflet';
import { findDOMNode } from 'react-dom';
import MiniMap from 'leaflet-minimap';

import 'leaflet.Zoomify';


const size = 35000;
const tiles = '/static/dist/tiles/';


export default class extends Component {


  /**
   * Render the image, bind events.
   */
  componentDidMount() {
    this._initLeaflet();
    this._bindEvents();
  }


  /**
   * Spin up the leaflet instance.
   */
  _initLeaflet() {

    let el = findDOMNode(this.refs.image);

    this.map = L.map(el, {
      crs: L.CRS.Simple,
      attributionControl: false,
      zoomControl: false,
    });

    // Zoom buttons.
    let zoomControl = L.control.zoom({
      position: 'topright',
    });

    // Image layer.
    let layer = L.tileLayer.zoomify(tiles, {
      width: size,
      height: size,
    });

    // Mini map layer.
    let miniLayer = L.tileLayer.zoomify(tiles, {
      width: size,
      height: size,
    });

    let miniMap = new MiniMap(miniLayer);

    this.map.setView([0, 0], 1);
    this.map.addControl(zoomControl);
    this.map.addLayer(layer);
    this.map.addControl(miniMap);

  }


  /**
   * Listen for map events.
   */
  _bindEvents() {

    // When the map is moved.
    this.map.on('moveend', _.bind(this.onMove, this));

  }


  /**
   * Update the route when the map is moved.
   */
  onMove() {
    console.log('move');
  }


  /**
   * Render the image container.
   */
  render() {
    return <div id="image" ref="image"></div>;
  }


}
