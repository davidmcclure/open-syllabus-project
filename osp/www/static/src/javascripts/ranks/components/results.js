

import _ from 'lodash';
import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import TextList from './text-list';


@connect(
  state => state.results
)
export default class extends Component {


  /**
   * Render the ranking results.
   */
  render() {

    let content;

    if (this.props.hits.length) {
      content = (
        <TextList
          totalHits={this.props.totalHits}
          hits={this.props.hits}
        />
      );
    }

    return (
      <div id="results">
        {content}
      </div>
    );

  }


}
