

import React, { Component } from 'react';
import { connect } from 'react-redux';
import { createHistory, useQueries } from 'history';
import Qs from 'qs';

import * as actions from '../actions/results';
import { makeQueryString } from '../utils';


@connect(
  state => ({
    filters: state.filters
  }),
  actions
)
export default class extends Component {


  /**
   * Listen for fragment changes.
   */
  componentDidMount() {

    this.history = useQueries(createHistory)();

    this.history.listen(loc => {
      // load results
    });

    this.setHash();

  }


  /**
   * Listen for fragment changes.
   */
  componentDidUpdate() {
    this.setHash();
  }


  setHash() {

    this.history.push({
      query: this.props.filters
    })

  }


  render() {
    return null;
  }


}
