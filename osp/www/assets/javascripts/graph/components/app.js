

import React, { Component } from 'react';

import Image from './image';
import Header from './header';


export default class extends Component {


  /**
   * Render the application.
   */
  render() {
    return (
      <div className="wrapper">
        <Image />
        <Header />
      </div>
    );
  }


}
