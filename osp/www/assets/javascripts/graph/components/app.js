

import React, { Component } from 'react';

import Image from './image';
import Router from './router';


export default class extends Component {


  /**
   * Render the application.
   */
  render() {
    return (
      <div className="wrapper">
        <Image />
        <Router />
      </div>
    );
  }


}
