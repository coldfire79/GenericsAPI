module KBaseExperiments {

    /* A boolean - 0 for false, 1 for true.
      @range (0, 1)
    */
    typedef int bool;

     /* Ref to a genome
        @id ws KBaseGenomes.Genome
     */
     typedef string GenomeRef;

     /* Ref to a Tree
        @id ws KBaseTrees.Tree
     */
     typedef string TreeRef;

     /* Ref to a ConditionSet
        @id ws KBaseExperiments.ConditionSet
     */
     typedef string ConditionSetRef;

     /* Ref to a WS object
        @id ws
     */
     typedef string WSRef;

    /*
        Internally this is used to store factor information (without the value term) and also a
        format for returning data in a useful form from get_conditions
        @optional unit unit_ont_id unit_ont_ref value
    */

    typedef structure{
        string factor;
        string factor_ont_ref;
        string factor_ont_id;
        string unit;
        string unit_ont_ref;
        string unit_ont_id;
        string value;
    } Factor;

    /*
     factors - list of supplied factors
     conditions - mapping of condition_labels to a list of factor values in the same order as the factors array
     ontology_mapping_method - One of “User curation”, “Closest matching string”
     @metadata ws ontology_mapping_method as Mapping Method
     @metadata ws length(factors) as Number of Factors
     @metadata ws length(conditions) as Number of Conditions
    */
     typedef structure{
    	mapping<string, list<string>> conditions;
    	list<Factor> factors;
	    string ontology_mapping_method;
     } ConditionSet;

    /*
        This stores categorical values (in which case the unit information will not be used) and
        is also a return format for attributes
        @optional value_ont_ref value_ont_id unit unit_ont_id unit_ont_ref
    */

    typedef structure{
        string value;
        string value_ont_ref;
        string value_ont_id;
        string unit;
        string unit_ont_ref;
        string unit_ont_id;
    } AttributeValue;

    /*
        Internally this is used to store attribute information. Categorical attributes will possess a
        categories field mapping all values. Quantitative attributes should possess unit information
        @optional unit unit_ont_id unit_ont_ref categories
    */

    typedef structure{
        string attribute;
        string attribute_ont_ref;
        string attribute_ont_id;
        string unit;
        string unit_ont_ref;
        string unit_ont_id;
        mapping<string, AttributeValue> categories;
    } Attribute;

    /*
     factors - list of supplied factors
     conditions - mapping of instance_labels to a list of attribute values in the same order as
     the attributes array

     ontology_mapping_method - One of “User curation”, “Closest matching string”

     @metadata ws ontology_mapping_method as Mapping Method
     @metadata ws length(attributes) as Number of Attributes
     @metadata ws length(instances) as Number of Instances
    */
     typedef structure{
    	mapping<string, list<string>> instances;
    	list<Attribute> attributes;
	    string ontology_mapping_method;
     } AttributeMapping;


     /*
        id_to_data_position - simple representation of a cluster, which maps features/conditions of the cluster to the
        row/col index in the data (0-based index).  The index is useful for fast lookup of data
        for a specified feature/condition in the cluster.
        id_to_condition - links to a specific condition in the associated ConditionSet

        @optional id_to_condition
    */
    typedef structure {
        mapping<string, int> id_to_data_position;
        mapping<string, string> id_to_condition;
    } labeled_cluster;

    /*
        A set of clusters, typically generated for a Float2DMatrix wrapper, such as Expression
        data or single feature knockout fitness data.

        clusters - list of clusters
        original_data - pointer to the original data used to make this cluster set
        tree_ref - pointer to the tree associated with this ClusterSet (if any)
        condition_set_ref - pointer to a condition set for this axis (if any)
        genome_ref - pointer to a genome for this axis (if any)

        @metadata ws length(clusters) as n_clusters
        @metadata ws original_data as Source Data
        @metadata ws tree_ref as Associated Tree
        @metadata ws condition_set_ref as Associated Conditions
        @metadata ws genome_ref as Associated Genome

        @optional tree_ref condition_set_ref genome_ref
    */
    typedef structure {
        list<labeled_cluster> clusters;
        mapping<string, string> clustering_parameters;
        WSRef original_data;
        TreeRef tree_ref;
        WSRef condition_set_ref;
        GenomeRef genome_ref;
    } ClusterSet;

    /*
      A simple 2D matrix of floating point numbers with labels/ids for rows and
      columns.  The matrix is stored as a list of lists, with the outer list
      containing rows, and the inner lists containing values for each column of
      that row.  Row/Col ids should be unique.

      row_ids - unique ids for rows.
      col_ids - unique ids for columns.
      values - two dimensional array indexed as: values[row][col]
      @metadata ws length(row_ids) as n_rows
      @metadata ws length(col_ids) as n_cols
    */
    typedef structure {
      list<string> row_ids;
      list<string> col_ids;
      list<list<float>> values;
    } FloatMatrix2D;

    /*
      A wrapper around a FloatMatrix2D designed for simple matricies of pairwise Correlation data.

      KBaseMatrices Fields:
      description - short optional description of the dataset
      coefficient_data - contains pairwise correlation coefficient values
      significance_data - contains pairwise significance values

      Additional Fields:
      genome_ref - a reference to the aligned genome
      feature_mapping - map from row_id to a set feature ids in the genome

      Validation:
      @unique coefficient_data.row_ids
      @unique coefficient_data.col_ids
      @unique significance_data.row_ids
      @unique significance_data.col_ids

      @optional description correlation_parameters
      @optional genome_ref feature_mapping
      @optional significance_data

      @metadata ws genome_ref as genome
      @metadata ws length(coefficient_data.row_ids) as matrix_size
    */
    typedef structure {
      string description;
      mapping<string, string> correlation_parameters;
      GenomeRef genome_ref;
      mapping<string, list<string>> feature_mapping;
      FloatMatrix2D coefficient_data;
      FloatMatrix2D significance_data;
    } CorrelationMatrix;

    /*
      Represents a node in a network.
      string label - String representation of a node
      mapping<string,string> properties - Other node properties

      @optional properties
    */
    typedef structure {
      string label;
      mapping<string, string> properties;
    } Node;

    /* Identifier of a node */
    typedef string node_id;

    /*
      Represents an edge in a network.
      node_id node_1 - Identifier (key of Network.nodes) of the first node (source node, if the edge is directed) connected by a given edge 
      node_id node_2 - Identifier (key of Network.nodes) of the second node (target node, if the edge is directed) connected by a given edge
      boolean directed - Specify whether the edge is directed or not. 1 if it is directed, 0 if it is not directed
      float weight - Weight of an edge
      string label - String representation of an edge
      mapping<string,string> properties - Other edge properties

      @optional directed weight label properties
    */
    typedef structure {
      node_id node_1_id;
      node_id node_2_id;
      bool directed;
      float weight;
      string label;
      mapping<string, string> properties;
    } Edge;

    /*
      Represents a network
      list<Edge> edges - A list of all edges in a network
      mapping<node_id, Node>> nodes - A dict of all nodes in a network
      mapping<string,string> network_properties - Other network properties

      @optional description network_properties

      @metadata ws length(nodes) as n_nodes
      @metadata ws length(edges) as n_edges
    */
    typedef structure {
      string description;
      list<Edge> edges;
      mapping<node_id, Node> nodes;
      mapping<string, string> network_properties;
    } Network;
};