

import React, { Component, PropTypes } from 'react';


export default class extends Component {


  static propTypes = {
    option: PropTypes.object.isRequired,
  };


  /**
   * Render a filter option.
   */
  render() {

    let count = this.props.option.count.toLocaleString();

    return (
      <div className="filter-option">

        <span className="count">
          (<strong>{count}</strong>)
        </span>

        {' '}

        <span className="value">
          {this.props.option.label}
        </span>

      </div>
    );

  }


}
