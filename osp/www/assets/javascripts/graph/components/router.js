

import { connect } from 'react-redux';
import React, { Component } from 'react';
import { Router } from 'director';

import * as actions from '../actions/route';


@connect(null, actions)
export default class extends Component {


  /**
   * Initialize the router.
   */
  componentDidMount() {

    this.router = Router({
      '/:x/:y/:z': (x, y, z) => {
        console.log(x, y, z);
      }
    });

    this.router.init();

  }


  render() {
    return null;
  }


}
