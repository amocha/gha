locals {
  dateCreated = formatdate("DD-MMM-YYYY hh:mm:ss ZZZ", timestamp())

  // subnet_ids     = var.placement == "PUB" ? var.isprod == false ? [module.defaultsub[0].subnetdetails, module.appsvcsub[0].subnetdetails] : [module.defaultsub[0].subnetdetails, module.appsvcsub[0].subnetdetails, module.defaultsub[1].subnetdetails, module.appsvcsub[1].subnetdetails] : [module.defaultprvsub[0].subnetdetails, module.appsvcprvsub[0].subnetdetails]
  //€ý,€ý,€ý,€ý, kube_subnetids = var.isprod == true ? ["/subscriptions/${var.prdsub}/resourceGroups/DP-PUB-MGMT-PRD-1.0.0-AKS-nodepools-rg/providers/Microsoft.Network/virtualNetworks/aks-vnet-19100102/subnets/aks-subnet"] : ["/subscriptions/${var.npdsub}/resourceGroups/DP-PUB-MGMT-NPD-1.0.0-AKS-nodepools-rg/providers/Microsoft.Network/virtualNetworks/aks-vnet-19100102/subnets/aks-subnet"]
  prim_tags = merge(module.tag.tags_without_location, { "location" = module.tag.location_primary, "dateCreated" = local.dateCreated }, var.tags)
  sec_tags  = merge(module.tag.tags_without_location, { "location" = module.tag.location_secondary, "dateCreated" = local.dateCreated }, var.tags)
  tags      = var.isprod == true ? [local.prim_tags, local.sec_tags] : [local.prim_tags]
  mgmtaccesspol = { mgmtaccesspol = {
    tenant_id               = data.azurerm_client_config.terraform.tenant_id
    object_id               = data.azurerm_client_config.terraform.object_id
    certificate_permissions = ["get", "list", "create", "delete", "update", "import"]
    key_permissions         = ["get", "create", "update", "list", "delete"]
    secret_permissions      = ["get", "list", "set", "delete"]
    storage_permissions     = ["get", "list"]
  } }

  useridentityaccesspol = { useridentityaccesspol = {
    tenant_id               = data.azurerm_client_config.terraform.tenant_id
    object_id               = azurerm_user_assigned_identity.useridentity.principal_id
    certificate_permissions = ["get", "list"]
    key_permissions         = ["get", "create", "list"]
    secret_permissions      = ["get", "list"]
    storage_permissions     = ["get", "list"]
  } }
  access_pol      = merge(var.access_pol, local.mgmtaccesspol, var.additional_access_pol, local.useridentityaccesspol)
  wkstm           = var.workStream == "" ? "" : "-${var.workStream}"
  app_resource_gp = var.isprod == true ? ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-app-rg", "${var.projectStream}${local.wkstm}-${var.placement}-s-${var.environment}-${var.releaseVersion}-${var.instance}-app-rg"] : ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-app-rg"]
  resource_gp     = var.isprod == true ? ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-rg", "${var.projectStream}${local.wkstm}-${var.placement}-s-${var.environment}-${var.releaseVersion}-${var.instance}-rg"] : ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-rg"]
  appsp_win_rg    = var.isprod == true ? ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-appspwin-rg", "${var.projectStream}${local.wkstm}-${var.placement}-s-${var.environment}-${var.releaseVersion}-${var.instance}-appspwin-rg"] : ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-appspwin-rg"]
  appsp_lnx_rg    = var.isprod == true ? ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-appsplnx-rg", "${var.projectStream}${local.wkstm}-${var.placement}-s-${var.environment}-${var.releaseVersion}-${var.instance}-appsplnx-rg"] : ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-appsplnx-rg"]
  appsp_win       = var.isprod == true ? ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-appspwin", "${var.projectStream}${local.wkstm}-${var.placement}-s-${var.environment}-${var.releaseVersion}-${var.instance}-appspwin"] : ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-appspwin"]
  appsp_lnx       = var.isprod == true ? ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-appsplnx", "${var.projectStream}${local.wkstm}-${var.placement}-s-${var.environment}-${var.releaseVersion}-${var.instance}-appsplnx"] : ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-appsplnx"]

  location = var.isprod == true ? [module.tag.location_primary, module.tag.location_secondary] : [module.tag.location_primary]

  loc_short_prim  = lookup(module.tag.region_short, module.tag.location_primary)
  loc_short_sec   = lookup(module.tag.region_short, module.tag.location_secondary)
  vnet            = var.placement == "PRV" ? [] : var.isprod == true ? [var.vnet_prim, var.vnet_sec] : [var.vnet_prim]
  vnetname        = var.placement == "PRV" ? [] : var.isprod == true ? ["${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-${local.loc_short_prim}-vn-${var.instance}", "${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-${local.loc_short_sec}-vn-${var.instance}"] : ["${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-${local.loc_short_prim}-vn-${var.instance}"]
  vnetlocation    = var.placement == "PRV" ? [] : var.isprod == true ? [module.tag.location_primary, module.tag.location_secondary] : [module.tag.location_primary]
  vnettags        = var.placement == "PRV" ? [] : var.isprod == true ? [local.prim_tags, local.sec_tags] : [local.prim_tags]
  defsub          = var.isprod == true ? ["${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-${local.loc_short_prim}-defsub-${var.instance}", "${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-${local.loc_short_sec}-defsub-${var.instance}"] : ["${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-${local.loc_short_prim}-defsub-${var.instance}"]
  appsvcsub       = var.isprod == true ? ["${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-${local.loc_short_prim}-appsvc-${var.instance}", "${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-${local.loc_short_sec}-appsvc-${var.instance}"] : ["${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-${local.loc_short_prim}-appsvc-${var.instance}"]
  defuseridentity = "${var.projectStream}${var.workStream}${var.environment}def001"
  defprvsub       = "${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${local.loc_short_prim}-defsub-${var.instance}"
  appsvcprvsub    = "${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${local.loc_short_prim}-appsvc-${var.instance}"

  // linux_appsp = var.appsptype == "linux" ? 1 : var.appsptype == "both" ? 1 : 0
  // win_appsp = var.appsptype == "windows" ? 1 : var.appsptype == "both" ? 1 : 0
  linux_appsp = var.isprod == true ? var.appsptype == "linux" ? 2 : var.appsptype == "both" ? 2 : 0 : var.appsptype == "linux" ? 1 : var.appsptype == "both" ? 1 : 0
  win_appsp   = var.isprod == true ? var.appsptype == "windows" ? 2 : var.appsptype == "both" ? 2 : 0 : var.appsptype == "windows" ? 1 : var.appsptype == "both" ? 1 : 0
  kvname      = "${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-kv${var.instance}"
}
