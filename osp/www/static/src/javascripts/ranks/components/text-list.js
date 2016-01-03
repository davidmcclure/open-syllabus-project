

import _ from 'lodash';
import classNames from 'classnames';
import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import TextRow from './text-row';
import SKCircle from './sk-circle';


@connect(state => state.results)
export default class extends Component {


  /**
   * Render the ranking table.
   */
  render() {

    let texts, spinner;

    // If texts are returned, render the list.

    if (this.props.hits.length) {

      // Build the text list.
      let rows = _.map(this.props.hits, function(h, i) {
        return <TextRow key={h._id} hit={h} rank={i+1} />
      });

      // Table classes.
      let tableCx = classNames('table', 'table-hover', {
        loading: this.props.loading,
      });

      texts = (
        <table className={tableCx}>

          <thead>
            <tr>
              <th>Rank</th>
              <th>Count</th>
              <th>Text</th>
            </tr>
          </thead>

          <tbody>
            {rows}
          </tbody>

        </table>
      );

    }

    // Otherwise, show an empty-set icon.

    else if (!this.props.loading) {
      texts = <i className="fa fa-ban"></i>;
    }

    // During load, show a spinner.

    if (this.props.loading) {
      spinner = <div className="spinner"><SKCircle /></div>;
    }

    return (
      <div id="text-list">
        {texts}
        {spinner}
      </div>
    );

  }


}
