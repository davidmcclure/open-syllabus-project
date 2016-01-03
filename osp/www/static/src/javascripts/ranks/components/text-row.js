

import React, { Component, PropTypes } from 'react';


export default class extends Component {


  static propTypes = {
    hit: PropTypes.object.isRequired,
    rank: PropTypes.number.isRequired,
  }


  /**
   * Render a text row.
   */
  render() {
    return (
      <tr className="text-row">

        <td className="rank">
          {this.props.rank}
        </td>

        <td className="count">
          {this.props.hit.sort[0]}
        </td>

        <td className="text">
          {this.props.hit._source.title}
        </td>

      </tr>
    );
  }


}
