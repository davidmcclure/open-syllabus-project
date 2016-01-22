

import { connect } from 'react-redux';
import React, { Component} from 'react';

import * as actions from '../actions/filters';


@connect(
  state => state.results,
  actions
)
export default class extends Component {


  /**
   * Render the "Load more" button.
   */
  render() {

    if (this.props.hits.length == this.props.hitCount) {
      return null;
    }

    return (
      <div id="load-more">

        <button
          onClick={this.props.loadNextPage}
        >Load More</button>

      </div>
    );

  }


}
