

import _ from 'lodash';
import React, { Component } from 'react';
import { connect } from 'react-redux';

import * as actions from '../actions/filters';


@connect(
  state => ({
    filters: state.filters,
    loading: state.results.loading,
  }),
  actions,
)
export default class extends Component {


  /**
   * Render the "Clear Filters" button.
   */
  render() {

    // Are all filters empty?
    let empty = _(this.props.filters).values().every(_.isEmpty);

    return (empty || this.props.loading) ? null : (

      <div id="clear-filters">

        <button
          className="btn btn-xs btn-danger"
          onClick={this.props.clearFilters}>

          <i className="fa fa-times"></i>{' '}
          Clear all filters

        </button>

      </div>

    );

  }


}
