

import _ from 'lodash';


export default class {


  /**
   * Set the raw hit.
   *
   * @param {Object} hit
   */
  constructor(hit) {
    this.hit = hit;
  }


  /**
   * Get the citation count.
   *
   * @return {Number}
   */
  count() {
    return this.hit.sort[0];
  }


  /**
   * Get a document field.
   *
   * @param {String} key
   * @return {String}
   */
  field(key, delimiter=', ') {

    // Try to get a highlight.
    let value = (
      _.get(this.hit, `highlight.${key}`) ||
      _.get(this.hit, `_source.${key}`)
    );

    // Join arrays into a single string.
    return _.isArray(value) ? value.join(delimiter) : value;

  }


}
