

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
   * Get a document field.
   *
   * @param {String} key
   * @return {String}
   */
  field(key, delimiter=', ') {

    // Try to find a highlight.
    let value = (
      _.get(this.hit, `highlight.${key}`) ||
      _.get(this.hit, `_source.${key}`)
    );

    // Join arrays into a string.
    return _.isArray(value) ? value.join(delimiter) : value;

  }


  /**
   * Get the citation count.
   *
   * @return {Number}
   */
  get count() {
    return this.hit.sort[0];
  }


}
