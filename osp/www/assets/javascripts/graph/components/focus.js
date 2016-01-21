

import React, { Component, PropTypes } from 'react';


export default class extends Component {


  static contextTypes = {
    map: PropTypes.object.isRequired,
  };


  /**
   * Focus the map.
   */
  componentDidUpdate() {
    console.log(focus);
  }


  render() {
    return null;
  }


}
