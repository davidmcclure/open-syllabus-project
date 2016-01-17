

import _ from 'lodash';
import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import HitCount from './hit-count';
import ClearFilters from './clear-filters';
import Search from './search';
import TextList from './text-list';

import * as actions from '../actions/results';


@connect(
  state => ({
    filters: state.filters
  }),
  actions
)
export default class extends Component {


  /**
   * Query for initial results.
   */
  componentDidMount() {
    this.props.loadResults(this.props.filters);
  }


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
        <HitCount />
        <ClearFilters />
        <Search />
        <TextList />
      </div>
    );
  }


}
