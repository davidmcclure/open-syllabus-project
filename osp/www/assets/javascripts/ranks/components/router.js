

import { connect } from 'react-redux';
import React, { Component } from 'react';
import { createHistory } from 'history';

import * as actions from '../actions/results';


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

    this.history = createHistory();

    this.history.listen(function(loc) {
      // parse QS, call loadResults()
      console.log('change');
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
    console.log('set hash', this.props.filters);
  }


  render() {
    return null;
  }


}
