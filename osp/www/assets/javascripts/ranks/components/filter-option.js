

import React, { Component, PropTypes } from 'react';


export default class extends Component {


  static propTypes = {
    option: PropTypes.object.isRequired,
  }


  /**
   * Render a filter option.
   */
  render() {

    let count = this.props.option.count.toLocaleString();

    return (
      <div className="filter-option">
        (<strong>{count}</strong>){' '}
        {this.props.option.label}
      </div>
    );

  }


}
