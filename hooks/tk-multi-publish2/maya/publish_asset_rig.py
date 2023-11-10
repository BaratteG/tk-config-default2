"""
Need to add the hook python file in the config.env.includes.settings.tk-multi-publish2.yml
"""


import os
import maya.cmds as cmds
import maya.mel as mel
import sgtk
import inspect

from tank_vendor import six

from pipelineFramework.maya.shotgrid.publishPlugins.accepts        import AcceptAssetLOD
from pipelineFramework.maya.shotgrid.publishPlugins.validates      import ValidateAssetLOD
from pipelineFramework.maya.shotgrid.publishPlugins.publishes      import PublishRig

# Inherit from {self}/publish_file.py 
# Check config.env.includes.settings.tk-multi-publish2.yml
HookBaseClass = sgtk.get_hook_baseclass()


class MayaAssetRigPublishPlugin(HookBaseClass):

    def accept(self, settings, item):

        acceptor = AcceptAssetLOD(hookClass=self)
        return acceptor.accept(
            settings,
            item,
            self.publishTemplate,
            self.propertiesPublishTemplate
        )

    def validate(self, settings, item):

        validator = ValidateAssetLOD(hookClass=self)
        validator.validate(
            item,
            self.propertiesPublishTemplate,
            isChild=True
        )

        # run the base class validation
        return super(MayaAssetRigPublishPlugin, self).validate(settings, item)


    def publish(self, settings, item):

        publishator = PublishRig(hookClass=self)
        publishator.publish(
            item,
            isChild=True
        )

        # let the base class register the publish
        super(MayaAssetRigPublishPlugin, self).publish(settings, item)

    @property
    def publishTemplate(self):
        return "Asset Rig Publish Template"

    @property
    def propertiesPublishTemplate(self):
        return "asset_rig_publish_template"

    @property
    def description(self):
        return """
        <p>This plugin publish the selected assets for the model pipeline step
        You need to select root transform of the asset.</p>
        """

    @property
    def settings(self):
        # inherit the settings from the base publish plugin
        base_settings = super(MayaAssetRigPublishPlugin, self).settings or {}

        # settings specific to this class
        maya_publish_settings = {
            self.publishTemplate : {
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
        return ["maya.asset.rig"]