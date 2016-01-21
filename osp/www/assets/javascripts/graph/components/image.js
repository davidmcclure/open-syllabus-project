

import L from 'leaflet';
import { findDOMNode } from 'react-dom';
import React, { Component } from 'react';
import MiniMap from 'leaflet-minimap';
import 'leaflet.Zoomify';

import history from '../history';
import config from './image.yml';


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
    let layer = L.tileLayer.zoomify(config.tiles, {
      width:  config.size,
      height: config.size,
    });

    // Mini map layer.
    let miniLayer = L.tileLayer.zoomify(config.tiles, {
      width:  config.size,
      height: config.size,
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
   * Set the route on move.
   */
  onMove() {

    let c = this.map.getCenter();
    let z = this.map.getZoom();

    var x = c.lng.toFixed(4);
    var y = c.lat.toFixed(4);

    history.replace({
      pathname: `${x}/${y}/${z}`
    });

  }


  /**
   * Render the image container.
   */
  render() {
    return <div id="image" ref="image"></div>;
  }


}
