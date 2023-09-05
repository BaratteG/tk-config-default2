
import os
import maya.cmds as cmds
import maya.mel as mel
import sgtk

from tank_vendor import six

from pipelineFramework.maya.hookPublishs    import HookPublishAlembic
hooksPublish = HookPublishAlembic()

HookBaseClass = sgtk.get_hook_baseclass()

class MayaAssetAlembicLOPublishPlugin(HookBaseClass):

    def accept(self, settings, item):

        return hooksPublish.acceptLOD(
            self,
            settings,
            item,
            self.publishTemplate,
            self.propertiesPublishTemplate
        )

    def validate(self, settings, item):

        hooksPublish.validate(
            self,
            settings,
            item,
            self.propertiesPublishTemplate,
            isChild=True
        )

        # run the base class validation
        return super(MayaAssetAlembicLOPublishPlugin, self).validate(settings, item)

    def publish(self, settings, item):

        hooksPublish.publishAlembicLOD(
            self,
            settings,
            item,
            isChild=True
        )

        # let the base class register the publish
        super(MayaAssetAlembicLOPublishPlugin, self).publish(settings, item)

    @property
    def publishTemplate(self):
        return "Asset Alembic LO Publish Template"

    @property
    def propertiesPublishTemplate(self):
        return "asset_alembic_lo_publish_template"

    @property
    def description(self):
        return """
        <p>This plugin publish the selected assets for the model pipeline step
        You need to select root transform of the asset.</p>
        """

    @property
    def settings(self):
        # inherit the settings from the base publish plugin
        base_settings = super(MayaAssetAlembicLOPublishPlugin, self).settings or {}

        # settings specific to this class
        maya_publish_settings = {
            self.publishTemplate: {
                "type": "template",
                "default": None,
                "description": "Template path for published work files. Should"
                "correspond to a template defined in "
                "templates.yml.",
            }      
        }

        # update the base settings
        base_settings.update(maya_publish_settings)

        return base_settings

    @property
    def item_filters(self):
        return ["maya.asset.alembicLO"]

def _session_path():
    """
    Return the path to the current session
    :return:
    """
    path = cmds.file(query=True, sn=True)

    if path is not None:
        path = six.ensure_str(path)

    return path


def _get_save_as_action():
    """
    Simple helper for returning a log action dict for saving the session
    """

    engine = sgtk.platform.current_engine()

    # default save callback
    callback = cmds.SaveScene

    # if workfiles2 is configured, use that for file save
    if "tk-multi-workfiles2" in engine.apps:
        app = engine.apps["tk-multi-workfiles2"]
        if hasattr(app, "show_file_save_dlg"):
            callback = app.show_file_save_dlg

    return {
        "action_button": {
            "label": "Save As...",
            "tooltip": "Save the current session",
            "callback": callback,
        }
    }