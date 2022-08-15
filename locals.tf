locals {
  dateCreated = formatdate("DD-MMM-YYYY hh:mm:ss ZZZ", timestamp())

  prim_tags = merge(module.tag.tags_without_location, { "location" = module.tag.location_primary, "dateCreated" = local.dateCreated }, var.tags)
  sec_tags  = merge(module.tag.tags_without_location, { "location" = module.tag.location_secondary, "dateCreated" = local.dateCreated }, var.tags)
  tags      = var.isProd == true ? [local.prim_tags, local.sec_tags] : [local.prim_tags]
  mgmtaccesspol = { mgmtaccesspol = {
    tenant_id               = data.azurerm_client_config.terraform.tenant_id
    object_id               = data.azurerm_client_config.terraform.object_id
    certificate_permissions = ["Get", "List", "Create", "Delete", "Update", "Import"]
    key_permissions         = ["Get", "Create", "Update", "List", "Delete"]
    secret_permissions      = ["Get", "List", "Set", "Delete"]
    storage_permissions     = ["Get", "List"]
  } }

  useridentityaccesspol = { useridentityaccesspol = {
    tenant_id               = data.azurerm_client_config.terraform.tenant_id
    object_id               = azurerm_user_assigned_identity.useridentity.principal_id
    certificate_permissions = ["Get", "List"]
    key_permissions         = ["Get", "Create", "List"]
    secret_permissions      = ["Get", "List"]
    storage_permissions     = ["Get", "List"]
  } }
  access_pol      = merge(var.access_pol, local.mgmtaccesspol, var.additional_access_pol, local.useridentityaccesspol)
  wkstm           = var.workStream == "" ? "" : "-${var.workStream}"
  app_resource_gp = var.isProd == true ? ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-app-rg", "${var.projectStream}${local.wkstm}-${var.placement}-s-${var.environment}-${var.releaseVersion}-${var.instance}-app-rg"] : ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-app-rg"]
  resource_gp     = var.isProd == true ? ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-rg", "${var.projectStream}${local.wkstm}-${var.placement}-s-${var.environment}-${var.releaseVersion}-${var.instance}-rg"] : ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-rg"]
  appsp_win_rg    = var.isProd == true ? ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-appspwin-rg", "${var.projectStream}${local.wkstm}-${var.placement}-s-${var.environment}-${var.releaseVersion}-${var.instance}-appspwin-rg"] : ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-appspwin-rg"]
  appsp_lnx_rg    = var.isProd == true ? ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-appsplnx-rg", "${var.projectStream}${local.wkstm}-${var.placement}-s-${var.environment}-${var.releaseVersion}-${var.instance}-appsplnx-rg"] : ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-appsplnx-rg"]
  appsp_win       = var.isProd == true ? ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-appspwin", "${var.projectStream}${local.wkstm}-${var.placement}-s-${var.environment}-${var.releaseVersion}-${var.instance}-appspwin"] : ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-appspwin"]
  appsp_lnx       = var.isProd == true ? ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-appsplnx", "${var.projectStream}${local.wkstm}-${var.placement}-s-${var.environment}-${var.releaseVersion}-${var.instance}-appsplnx"] : ["${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${var.releaseVersion}-${var.instance}-appsplnx"]

  location = var.isProd == true ? [module.tag.location_primary, module.tag.location_secondary] : [module.tag.location_primary]

  loc_short_prim  = lookup(module.tag.region_short, module.tag.location_primary)
  loc_short_sec   = lookup(module.tag.region_short, module.tag.location_secondary)
  vnet            = var.placement == "PRV" ? [] : var.isProd == true ? [var.vnet_prim, var.vnet_sec] : [var.vnet_prim]
  vnetname        = var.placement == "PRV" ? [] : var.isProd == true ? ["${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-${local.loc_short_prim}-vn-${var.instance}", "${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-${local.loc_short_sec}-vn-${var.instance}"] : ["${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-${local.loc_short_prim}-vn-${var.instance}"]
  vnetlocation    = var.placement == "PRV" ? [] : var.isProd == true ? [module.tag.location_primary, module.tag.location_secondary] : [module.tag.location_primary]
  vnettags        = var.placement == "PRV" ? [] : var.isProd == true ? [local.prim_tags, local.sec_tags] : [local.prim_tags]
  defsub          = var.isProd == true ? ["${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-${local.loc_short_prim}-defsub-${var.instance}", "${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-${local.loc_short_sec}-defsub-${var.instance}"] : ["${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-${local.loc_short_prim}-defsub-${var.instance}"]
  appsvcsub       = var.isProd == true ? ["${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-${local.loc_short_prim}-appsvc-${var.instance}", "${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-${local.loc_short_sec}-appsvc-${var.instance}"] : ["${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-${local.loc_short_prim}-appsvc-${var.instance}"]
  defuseridentity = "${var.projectStream}${var.workStream}${var.environment}def001"
  defprvsub       = "${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${local.loc_short_prim}-defsub-${var.instance}"
  appsvcprvsub    = "${var.projectStream}${local.wkstm}-${var.placement}-p-${var.environment}-${local.loc_short_prim}-appsvc-${var.instance}"

  // linux_appsp = var.appsptype == "linux" ? 1 : var.appsptype == "both" ? 1 : 0
  // win_appsp = var.appsptype == "windows" ? 1 : var.appsptype == "both" ? 1 : 0
  linux_appsp = var.isProd == true ? var.appsptype == "linux" ? 2 : var.appsptype == "both" ? 2 : 0 : var.appsptype == "linux" ? 1 : var.appsptype == "both" ? 1 : 0
  win_appsp   = var.isProd == true ? var.appsptype == "windows" ? 2 : var.appsptype == "both" ? 2 : 0 : var.appsptype == "windows" ? 1 : var.appsptype == "both" ? 1 : 0
  kvname      = "${var.projectStream}${local.wkstm}-${var.placement}-${var.environment}-kv${var.instance}"
}
