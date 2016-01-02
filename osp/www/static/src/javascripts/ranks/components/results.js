

import React, { Component } from 'react';
import { connect } from 'react-redux';

import * as actions from '../actions/results';


@connect(
  state => ({
    filters: state.filters
  }),
  actions,
)
export default class extends Component {


  /**
   * Query for new results when filters change.
   */
  componentDidUpdate() {
    this.props.loadResults(this.props.filters);
  }


  /**
   * Render the ranking results.
   */
  render() {
    return (
      <div id="results">
        <h1>results</h1>
      </div>
    );
  }


}
