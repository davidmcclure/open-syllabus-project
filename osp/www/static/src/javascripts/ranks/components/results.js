

import _ from 'lodash';
import React, { Component } from 'react';
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
      content = <TextList />
    }

    return (
      <div id="results">
        {content}
      </div>
    );

  }


}
