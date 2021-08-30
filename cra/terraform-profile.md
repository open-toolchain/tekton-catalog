# Configuring CRA-terraform profile file
CRA-terraform supports configuring the terraform scan and allows: 
1. Chosing rule parameters 
1. Chosing which rules to run 

## Structure of the configuration file

The content of the file is a JSON object with the following properties:
1. `"scc_goals"` - SCC goals to evaluate by goal ID.
1. `"scc_goal_parameters"` - Contains the parameters values for configurable SCC goals  

All properties are optional.

### `"scc_goals"` Definition:  
`"scc_goals"` is defined as a JSON array of `{ "scc_goal_id": "..." }`   
The value of `"scc_goal_id"` is the goal id as defined by SCC.  
For example if we would like to evalute SCC goal:  
`"Ensure Cloudant has at least # users with the IAM manager role"`  
we will define the following object:  
`{ "scc_goal_id": "3000111" }`  

### `"scc_goal_parameters"` Definition:
The acceptable properties which can be defined are listed bellow.  
The list maps between goal id with parameters and the definition of each parameter.  

### Example of SCC goal selection:  

```json
{
  "scc_goals": [
        { "scc_goal_id": "3000010" },
        { "scc_goal_id": "3000015" }
  ],
  "scc_goal_parameters": {
    "no_of_managers_for_cloudant_db": 4
  }
}   
```

### Where to place the configuration file
The configuration file should be placed in the terraform repo. 
The CRA-terraform parameter `policy-config-json` can be used to point to the configuration file location in the repository. 
If the parameter is not defined, CRA-Terraform will search for a default configuration file called `goal-list.json` in the directory specified in `tf-dir`.

## List of parameters and default values
Follows a list of parameters that can be used for SCC goals. 

**Note that not all the goals are implemented.**

Whenever alternative values are present in the list, the values of the parameter are limited to default or to the alternatives.

|goalId |parameter name |description |type |default |alternative values |
|---------|---------|---------|---------|---------|:----------:| 
|3000004|ibm_minimum_password_length|Minimum Password Length|number|12|['8']
|3000005|ibm_password_reuse_prevention|Password Reuse Prevention|number|24|unlimited
|3000021|allowed_admins_per_account|Maximum allowed administrators per account|number|10|unlimited
|3000024|api_keys_rotated_days|API Keys Rotated Days|number|90|unlimited
|3000025|account_owner_last_login_days|Account Owner Last Login Days|number|30|['90']
|3000029|no_of_admins_for_iam|Maximum no of IAM user administrators|number|3|unlimited
|3000032|no_of_service_id_admins_for_iam|Maximum no of IAM Service ID administrators|number|3|unlimited
|3000109|no_of_admins_for_cloudant_db|Maximum no of Cloudant DB user administrators|number|3|unlimited
|3000110|no_of_service_id_admins_for_cloudant_db|Maximum no of Cloudant DB Service IDs administrators|number|3|unlimited     
|3000233|hpcs_crypto_units|Hyper Protect Crypto Units|number|2|['3']
|3000235|hpcs_rotation_policy|Hyper Protect Crypto Keys Rotation Policy|number|1|['2', '3', '4', '5', '6', '7', '8', '9', '10']
|3000242|no_of_admins_for_redis_db|Maximum no of Redis DB user administrators|number|3|unlimited
|3000243|no_of_admins_for_postgresql_db|Maximum no of Postgresql DB user administrators|number|3|unlimited
|3000244|no_of_admins_for_mongo_db|Maximum no of Mongo DB user administrators|number|3|unlimited
|3000245|no_of_admins_for_elastic_search_db|Maximum no of Elastic Search DB user administrators|number|3|unlimited
|3000246|no_of_admins_for_etcd_db|Maximum no of ETCD user administrators|number|3|unlimited
|3000247|no_of_admins_for_key|Maximum no of Key user administrators|number|3|unlimited
|3000248|no_of_admins_for_kubernetes_container|Maximum no of Kubernetes Container user administrators|number|3|unlimited     
|3000249|no_of_admins_for_enterprise_db|Maximum no of Enterprise DB user administrators|number|3|unlimited
|3000251|no_of_service_id_admins_for_elastic_search_db|Maximum no of Elastic Search DB Service ID administrators|number|3|unlimited
|3000252|no_of_service_id_admins_for_key|Maximum no of Key Service ID administrators|number|3|unlimited
|3000253|no_of_service_id_admins_for_etcd_db|Maximum no of ETCD Service ID administrators|number|3|unlimited
|3000254|no_of_service_id_admins_for_kubernetes_container|Maximum no of Kubernetes Container Service ID administrators|number|3|unlimited
|3000255|no_of_service_id_admins_for_enterprise_db|Maximum no of Enterprise DB Service ID  administrators|number|3|unlimited 
|3000304|no_of_admins_for_monitoring|Maximum no of Monitoring user administrators|number|3|unlimited
|3000308|no_of_admins_for_logdna|Maximum no of LogDNA user administrators|number|3|unlimited
|3000309|no_of_service_id_admins_for_logdna|Maximum no of LogDNA ServiceID administrators|number|3|unlimited
|3000310|no_of_service_id_admins_for_monitoring|Maximum no of Monitoring Service ID administrators|number|3|unlimited        
|3000312|no_of_service_id_admins_for_mongo_db|Maximum no of Mongo DB Service ID administrators|number|3|unlimited
|3000313|no_of_service_id_admins_for_redis_db|Maximum no of Redis DB Service ID administrators|number|3|unlimited
|3000314|no_of_service_id_admins_for_postgresql_db|Maximum no of Postgresql DB Service ID administrators|number|3|unlimited  
|3000404|ssh_port|SSH Port|number|22|unlimited
|3000405|rdp_port|RDP Port|number|3389|unlimited
|3000409|iks_ingress_tls_versions|tlsVersion|number|1.2|['1.3']
|3000421|diffie_hellman_group|Diffie-Hellman Group|number|14|unlimited
|3000425|pre_shared_key|Pre-Shared Key|number|24|unlimited
|3000444|dns_port|DNS Port|number|53|unlimited
|3000453|vm_nic_count|VM NIC Count|number|1|unlimited
|3000601|scan_interval_max|Max Scan Interval Days|number|7|['10', '30']
|3000617|arbitrary_keys_rotated_days|Arbitrary Keys Rotated Days|number|90|unlimited
|3000618|username_password_keys_rotated_days|IAM credentials Keys Rotated Days|number|90|unlimited
|3000619|iam_credentials_keys_rotated_days|maxAPIKeyAge|number|90|unlimited
|3000621|no_of_admins_for_secrets_manager|Maximum no of Secrets Manager user administrators|number|3|unlimited
|3000622|no_of_admins_for_toolchain|Maximum no of Toolchain user administrators|number|3|unlimited
|3000623|no_of_admins_for_container_registry|Maximum no of Container Registry user administrators|number|3|unlimited
|3000628|no_of_service_id_admins_for_container_registry|Maximum no of Container Registry Service ID administrators|number|3|unlimited
|3000629|no_of_service_id_admins_for_tool_chain|Maximum no of Toolchain Service ID administrators|number|3|unlimited
|3000630|no_of_service_id_admins_for_secrets_manager|Maximum no of Secrets Manager Service ID administrators|number|3|unlimited
|3000724|access_tokens_expire|Access Tokens Expire Minutes|number|120|unlimited
|3000441|ssh_port|SSH Port|number|22|unlimited
|3000442|rdp_port|RDP Port|number|3389|unlimited
|3000038|iam_service_ids_max_count|Maximum allowed service ID with admin privilege per account|number|10|unlimited
|3000033|no_of_managers_for_iam|Minimum no of IAM managers|number|3|unlimited
|3000034|no_of_service_id_managers_for_iam|Minimum no of IAM Service ID managers|number|3|unlimited
|3000111|no_of_managers_for_cloudant_db|Minimum no of Cloudant database IAM managers|number|3|unlimited
|3000112|no_of_service_id_managers_for_cloudant_db|Minimum no of Cloudant database IAM Service ID managers|number|3|unlimited|3000256|no_of_managers_for_redis_db|Minimum no of Redis databases IAM managers|number|3|unlimited
|3000257|no_of_service_id_managers_for_redis_db|Minimum no of Redis databases IAM Servcie ID managers|number|3|unlimited     
|3000258|no_of_managers_for_postgresql_db|Minimum no of PostgreSQL databases IAM managers|number|3|unlimited
|3000259|no_of_service_id_managers_for_postgresql_db|Minimum no of PostgreSQL databases IAM Service ID managers|number|3|unlimited
|3000260|no_of_managers_for_mongo_db|Minimum no of MongoDB IAM managers|number|3|unlimited
|3000261|no_of_service_id_managers_for_mongo_db|Minimum no of MongoDB IAM Service ID managers|number|3|unlimited
|3000262|no_of_managers_for_elastic_search_db|Minimum no of Elastic Search IAM managers|number|3|unlimited
|3000263|no_of_service_id_managers_for_elastic_search_db|Minimum no of Elastic Search IAM Servcie ID managers|number|3|unlimited
|3000264|no_of_managers_for_etcd_db|Minimum no of etcd IAM managers|number|3|unlimited
|3000265|no_of_service_id_managers_for_etcd_db|Minimum no of etcd IAM Service ID managers|number|3|unlimited
|3000266|no_of_managers_for_key|Minimum no of Key IAM managers|number|3|unlimited
|3000267|no_of_service_id_managers_for_key|Minimum no of Key IAM Service ID managers|number|3|unlimited
|3000268|no_of_managers_for_kubernetes_container|Minimum no of Kubernetes Container IAM managers|number|3|unlimited
|3000269|no_of_service_id_managers_for_kubernetes_container|Minimum no of Kubernetes Container IAM Service ID managers|number|3|unlimited
|3000270|no_of_managers_for_enterprise_db|Minimum no of Enterprise DB IAM managers|number|3|unlimited
|3000271|no_of_service_id_managers_for_enterprise_db|Minimum no of Enterprise DB IAM Service ID managers|number|3|unlimited  
|3000315|no_of_managers_for_monitoring|Minimum no of Monitoring IAM managers|number|3|unlimited
|3000316|no_of_service_id_managers_for_monitoring|Minimum no of Monitoring IAM Service ID managers|number|3|unlimited        
|3000317|no_of_managers_for_logdna|Minimum no of LogDNA IAM managers|number|3|unlimited
|3000318|no_of_service_id_managers_for_logdna|Minimum no of LogDNA IAM Service ID managers|number|3|unlimited
|3000631|no_of_managers_for_secrets_manager|Minimum no of Secrets Manager IAM managers|number|3|unlimited
|3000632|no_of_service_id_managers_for_secrets_manager|Minimum no of Secrets Manager IAM Service ID managers|number|3|unlimited
|3000633|no_of_managers_for_toolchain|Minimum no of Toolchain IAM managers|number|3|unlimited
|3000634|no_of_service_id_managers_for_toolchain|Minimum no of Toolchain IAM Service ID managers|number|3|unlimited
|3000635|no_of_managers_for_container_registry|Minimum no of Container Registry IAM managers|number|3|unlimited
|3000636|no_of_service_id_managers_for_container_registry|Minimum no of Container Registry IAM Service ID managers|number|3|unlimited
