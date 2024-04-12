from typing import Any, Callable
import os
import json

DIRECTORY = os.path.dirname(__file__) + "/data/data/"


class MinecraftData:
    def __init__(self, platform: str, version: str) -> None:
        data_paths = MinecraftData.__get_data_paths()

        if platform not in data_paths:
            raise ValueError(
                f"Platform '{platform}' doesn't exist, " +
                "try one of the following: " +
                f"{', '.join(data_paths.keys())}"
            )

        if version not in data_paths[platform]:
            raise ValueError(
                f"Version '{version}' doesn't exist, " +
                "try one of the following: " +
                f"{', '.join(reversed(data_paths[platform].keys()))}"
            )

        self.platform = platform
        self.version = version

        self.data_paths = data_paths[platform][version]

    def __get_data_paths() -> dict[str, dict[str, dict[str, str]]]:
        data_paths = {}
        with open(DIRECTORY + "dataPaths.json") as data_paths_file:
            data_paths = json.load(data_paths_file)

        return data_paths

    def _get_platforms() -> list[str]:
        data_paths = MinecraftData.__get_data_paths()
        return list(data_paths.keys())

    def _get_versions(platform: str) -> list[str]:
        data_paths = MinecraftData.__get_data_paths()
        return list(data_paths[platform].keys())

    def _get_data(self, data_type: str) -> Any:
        data = []
        with open(DIRECTORY +
                  self.data_paths[data_type] +
                  f'/{data_type}.json') as file:
            data = json.load(file)

        return data

    def get_length(self, data_type: str) -> int:
        return len(self._get_data(data_type))

    def _get_all_match(self, data_type: str,
                       predicate: Callable) -> list[dict[str, Any]]:
        data = self._get_data(data_type)
        data_to_return = []

        if isinstance(data, dict):
            data = data.values()

        for x in data:
            if predicate(x):
                data_to_return.append(x)

        return data_to_return

    def _get_first_match(self, data_type: str, predicate: Callable):
        return next(x for x in self._get_data(data_type) if predicate(x))

    def _filter_by(self, key: str, value: Any) -> Callable[
            [dict[str, Any]], bool]:
        return lambda x: x[key] == value if key in x else False

    def get_first_item_by_enchantCategories(
            self, item_enchantCategories: Any) -> dict[str, Any]:
        """Get the item that matches the given enchantCategories

        Args:
            item_enchantCategories (Any): the enchantCategories to match to

        Returns:
            dict[str, Any]: the item that matches
        """
        return self._get_first_match(
            'items',
            self._filter_by('enchantCategories', item_enchantCategories)
        )

    def get_items_by_enchantCategories(
            self, item_enchantCategories: Any) -> list[dict[str, Any]]:
        """Get all items that match the given enchantCategories

        Args:
            item_enchantCategories (Any): the enchantCategories to match to

        Returns:
            list[dict[str, Any]]: the list of items that match
        """
        return self._get_all_match(
            'items',
            self._filter_by('enchantCategories', item_enchantCategories)
        )

    def get_first_item_by_stackSize(
            self, item_stackSize: Any) -> dict[str, Any]:
        """Get the item that matches the given stackSize

        Args:
            item_stackSize (Any): the stackSize to match to

        Returns:
            dict[str, Any]: the item that matches
        """
        return self._get_first_match(
            'items',
            self._filter_by('stackSize', item_stackSize)
        )

    def get_items_by_stackSize(
            self, item_stackSize: Any) -> list[dict[str, Any]]:
        """Get all items that match the given stackSize

        Args:
            item_stackSize (Any): the stackSize to match to

        Returns:
            list[dict[str, Any]]: the list of items that match
        """
        return self._get_all_match(
            'items',
            self._filter_by('stackSize', item_stackSize)
        )

    def get_first_item_by_displayName(
            self, item_displayName: Any) -> dict[str, Any]:
        """Get the item that matches the given displayName

        Args:
            item_displayName (Any): the displayName to match to

        Returns:
            dict[str, Any]: the item that matches
        """
        return self._get_first_match(
            'items',
            self._filter_by('displayName', item_displayName)
        )

    def get_items_by_displayName(
            self, item_displayName: Any) -> list[dict[str, Any]]:
        """Get all items that match the given displayName

        Args:
            item_displayName (Any): the displayName to match to

        Returns:
            list[dict[str, Any]]: the list of items that match
        """
        return self._get_all_match(
            'items',
            self._filter_by('displayName', item_displayName)
        )

    def get_first_item_by_name(
            self, item_name: Any) -> dict[str, Any]:
        """Get the item that matches the given name

        Args:
            item_name (Any): the name to match to

        Returns:
            dict[str, Any]: the item that matches
        """
        return self._get_first_match(
            'items',
            self._filter_by('name', item_name)
        )

    def get_items_by_name(
            self, item_name: Any) -> list[dict[str, Any]]:
        """Get all items that match the given name

        Args:
            item_name (Any): the name to match to

        Returns:
            list[dict[str, Any]]: the list of items that match
        """
        return self._get_all_match(
            'items',
            self._filter_by('name', item_name)
        )

    def get_first_item_by_maxDurability(
            self, item_maxDurability: Any) -> dict[str, Any]:
        """Get the item that matches the given maxDurability

        Args:
            item_maxDurability (Any): the maxDurability to match to

        Returns:
            dict[str, Any]: the item that matches
        """
        return self._get_first_match(
            'items',
            self._filter_by('maxDurability', item_maxDurability)
        )

    def get_items_by_maxDurability(
            self, item_maxDurability: Any) -> list[dict[str, Any]]:
        """Get all items that match the given maxDurability

        Args:
            item_maxDurability (Any): the maxDurability to match to

        Returns:
            list[dict[str, Any]]: the list of items that match
        """
        return self._get_all_match(
            'items',
            self._filter_by('maxDurability', item_maxDurability)
        )

    def get_first_item_by_repairWith(
            self, item_repairWith: Any) -> dict[str, Any]:
        """Get the item that matches the given repairWith

        Args:
            item_repairWith (Any): the repairWith to match to

        Returns:
            dict[str, Any]: the item that matches
        """
        return self._get_first_match(
            'items',
            self._filter_by('repairWith', item_repairWith)
        )

    def get_items_by_repairWith(
            self, item_repairWith: Any) -> list[dict[str, Any]]:
        """Get all items that match the given repairWith

        Args:
            item_repairWith (Any): the repairWith to match to

        Returns:
            list[dict[str, Any]]: the list of items that match
        """
        return self._get_all_match(
            'items',
            self._filter_by('repairWith', item_repairWith)
        )

    def get_first_item_by_id(
            self, item_id: Any) -> dict[str, Any]:
        """Get the item that matches the given id

        Args:
            item_id (Any): the id to match to

        Returns:
            dict[str, Any]: the item that matches
        """
        return self._get_first_match(
            'items',
            self._filter_by('id', item_id)
        )

    def get_items_by_id(
            self, item_id: Any) -> list[dict[str, Any]]:
        """Get all items that match the given id

        Args:
            item_id (Any): the id to match to

        Returns:
            list[dict[str, Any]]: the list of items that match
        """
        return self._get_all_match(
            'items',
            self._filter_by('id', item_id)
        )

    def get_first_block_by_filterLight(
            self, block_filterLight: Any) -> dict[str, Any]:
        """Get the block that matches the given filterLight

        Args:
            block_filterLight (Any): the filterLight to match to

        Returns:
            dict[str, Any]: the block that matches
        """
        return self._get_first_match(
            'blocks',
            self._filter_by('filterLight', block_filterLight)
        )

    def get_blocks_by_filterLight(
            self, block_filterLight: Any) -> list[dict[str, Any]]:
        """Get all blocks that match the given filterLight

        Args:
            block_filterLight (Any): the filterLight to match to

        Returns:
            list[dict[str, Any]]: the list of blocks that match
        """
        return self._get_all_match(
            'blocks',
            self._filter_by('filterLight', block_filterLight)
        )

    def get_first_block_by_boundingBox(
            self, block_boundingBox: Any) -> dict[str, Any]:
        """Get the block that matches the given boundingBox

        Args:
            block_boundingBox (Any): the boundingBox to match to

        Returns:
            dict[str, Any]: the block that matches
        """
        return self._get_first_match(
            'blocks',
            self._filter_by('boundingBox', block_boundingBox)
        )

    def get_blocks_by_boundingBox(
            self, block_boundingBox: Any) -> list[dict[str, Any]]:
        """Get all blocks that match the given boundingBox

        Args:
            block_boundingBox (Any): the boundingBox to match to

        Returns:
            list[dict[str, Any]]: the list of blocks that match
        """
        return self._get_all_match(
            'blocks',
            self._filter_by('boundingBox', block_boundingBox)
        )

    def get_first_block_by_minStateId(
            self, block_minStateId: Any) -> dict[str, Any]:
        """Get the block that matches the given minStateId

        Args:
            block_minStateId (Any): the minStateId to match to

        Returns:
            dict[str, Any]: the block that matches
        """
        return self._get_first_match(
            'blocks',
            self._filter_by('minStateId', block_minStateId)
        )

    def get_blocks_by_minStateId(
            self, block_minStateId: Any) -> list[dict[str, Any]]:
        """Get all blocks that match the given minStateId

        Args:
            block_minStateId (Any): the minStateId to match to

        Returns:
            list[dict[str, Any]]: the list of blocks that match
        """
        return self._get_all_match(
            'blocks',
            self._filter_by('minStateId', block_minStateId)
        )

    def get_first_block_by_stackSize(
            self, block_stackSize: Any) -> dict[str, Any]:
        """Get the block that matches the given stackSize

        Args:
            block_stackSize (Any): the stackSize to match to

        Returns:
            dict[str, Any]: the block that matches
        """
        return self._get_first_match(
            'blocks',
            self._filter_by('stackSize', block_stackSize)
        )

    def get_blocks_by_stackSize(
            self, block_stackSize: Any) -> list[dict[str, Any]]:
        """Get all blocks that match the given stackSize

        Args:
            block_stackSize (Any): the stackSize to match to

        Returns:
            list[dict[str, Any]]: the list of blocks that match
        """
        return self._get_all_match(
            'blocks',
            self._filter_by('stackSize', block_stackSize)
        )

    def get_first_block_by_material(
            self, block_material: Any) -> dict[str, Any]:
        """Get the block that matches the given material

        Args:
            block_material (Any): the material to match to

        Returns:
            dict[str, Any]: the block that matches
        """
        return self._get_first_match(
            'blocks',
            self._filter_by('material', block_material)
        )

    def get_blocks_by_material(
            self, block_material: Any) -> list[dict[str, Any]]:
        """Get all blocks that match the given material

        Args:
            block_material (Any): the material to match to

        Returns:
            list[dict[str, Any]]: the list of blocks that match
        """
        return self._get_all_match(
            'blocks',
            self._filter_by('material', block_material)
        )

    def get_first_block_by_states(
            self, block_states: Any) -> dict[str, Any]:
        """Get the block that matches the given states

        Args:
            block_states (Any): the states to match to

        Returns:
            dict[str, Any]: the block that matches
        """
        return self._get_first_match(
            'blocks',
            self._filter_by('states', block_states)
        )

    def get_blocks_by_states(
            self, block_states: Any) -> list[dict[str, Any]]:
        """Get all blocks that match the given states

        Args:
            block_states (Any): the states to match to

        Returns:
            list[dict[str, Any]]: the list of blocks that match
        """
        return self._get_all_match(
            'blocks',
            self._filter_by('states', block_states)
        )

    def get_first_block_by_displayName(
            self, block_displayName: Any) -> dict[str, Any]:
        """Get the block that matches the given displayName

        Args:
            block_displayName (Any): the displayName to match to

        Returns:
            dict[str, Any]: the block that matches
        """
        return self._get_first_match(
            'blocks',
            self._filter_by('displayName', block_displayName)
        )

    def get_blocks_by_displayName(
            self, block_displayName: Any) -> list[dict[str, Any]]:
        """Get all blocks that match the given displayName

        Args:
            block_displayName (Any): the displayName to match to

        Returns:
            list[dict[str, Any]]: the list of blocks that match
        """
        return self._get_all_match(
            'blocks',
            self._filter_by('displayName', block_displayName)
        )

    def get_first_block_by_diggable(
            self, block_diggable: Any) -> dict[str, Any]:
        """Get the block that matches the given diggable

        Args:
            block_diggable (Any): the diggable to match to

        Returns:
            dict[str, Any]: the block that matches
        """
        return self._get_first_match(
            'blocks',
            self._filter_by('diggable', block_diggable)
        )

    def get_blocks_by_diggable(
            self, block_diggable: Any) -> list[dict[str, Any]]:
        """Get all blocks that match the given diggable

        Args:
            block_diggable (Any): the diggable to match to

        Returns:
            list[dict[str, Any]]: the list of blocks that match
        """
        return self._get_all_match(
            'blocks',
            self._filter_by('diggable', block_diggable)
        )

    def get_first_block_by_emitLight(
            self, block_emitLight: Any) -> dict[str, Any]:
        """Get the block that matches the given emitLight

        Args:
            block_emitLight (Any): the emitLight to match to

        Returns:
            dict[str, Any]: the block that matches
        """
        return self._get_first_match(
            'blocks',
            self._filter_by('emitLight', block_emitLight)
        )

    def get_blocks_by_emitLight(
            self, block_emitLight: Any) -> list[dict[str, Any]]:
        """Get all blocks that match the given emitLight

        Args:
            block_emitLight (Any): the emitLight to match to

        Returns:
            list[dict[str, Any]]: the list of blocks that match
        """
        return self._get_all_match(
            'blocks',
            self._filter_by('emitLight', block_emitLight)
        )

    def get_first_block_by_name(
            self, block_name: Any) -> dict[str, Any]:
        """Get the block that matches the given name

        Args:
            block_name (Any): the name to match to

        Returns:
            dict[str, Any]: the block that matches
        """
        return self._get_first_match(
            'blocks',
            self._filter_by('name', block_name)
        )

    def get_blocks_by_name(
            self, block_name: Any) -> list[dict[str, Any]]:
        """Get all blocks that match the given name

        Args:
            block_name (Any): the name to match to

        Returns:
            list[dict[str, Any]]: the list of blocks that match
        """
        return self._get_all_match(
            'blocks',
            self._filter_by('name', block_name)
        )

    def get_first_block_by_maxStateId(
            self, block_maxStateId: Any) -> dict[str, Any]:
        """Get the block that matches the given maxStateId

        Args:
            block_maxStateId (Any): the maxStateId to match to

        Returns:
            dict[str, Any]: the block that matches
        """
        return self._get_first_match(
            'blocks',
            self._filter_by('maxStateId', block_maxStateId)
        )

    def get_blocks_by_maxStateId(
            self, block_maxStateId: Any) -> list[dict[str, Any]]:
        """Get all blocks that match the given maxStateId

        Args:
            block_maxStateId (Any): the maxStateId to match to

        Returns:
            list[dict[str, Any]]: the list of blocks that match
        """
        return self._get_all_match(
            'blocks',
            self._filter_by('maxStateId', block_maxStateId)
        )

    def get_first_block_by_harvestTools(
            self, block_harvestTools: Any) -> dict[str, Any]:
        """Get the block that matches the given harvestTools

        Args:
            block_harvestTools (Any): the harvestTools to match to

        Returns:
            dict[str, Any]: the block that matches
        """
        return self._get_first_match(
            'blocks',
            self._filter_by('harvestTools', block_harvestTools)
        )

    def get_blocks_by_harvestTools(
            self, block_harvestTools: Any) -> list[dict[str, Any]]:
        """Get all blocks that match the given harvestTools

        Args:
            block_harvestTools (Any): the harvestTools to match to

        Returns:
            list[dict[str, Any]]: the list of blocks that match
        """
        return self._get_all_match(
            'blocks',
            self._filter_by('harvestTools', block_harvestTools)
        )

    def get_first_block_by_resistance(
            self, block_resistance: Any) -> dict[str, Any]:
        """Get the block that matches the given resistance

        Args:
            block_resistance (Any): the resistance to match to

        Returns:
            dict[str, Any]: the block that matches
        """
        return self._get_first_match(
            'blocks',
            self._filter_by('resistance', block_resistance)
        )

    def get_blocks_by_resistance(
            self, block_resistance: Any) -> list[dict[str, Any]]:
        """Get all blocks that match the given resistance

        Args:
            block_resistance (Any): the resistance to match to

        Returns:
            list[dict[str, Any]]: the list of blocks that match
        """
        return self._get_all_match(
            'blocks',
            self._filter_by('resistance', block_resistance)
        )

    def get_first_block_by_drops(
            self, block_drops: Any) -> dict[str, Any]:
        """Get the block that matches the given drops

        Args:
            block_drops (Any): the drops to match to

        Returns:
            dict[str, Any]: the block that matches
        """
        return self._get_first_match(
            'blocks',
            self._filter_by('drops', block_drops)
        )

    def get_blocks_by_drops(
            self, block_drops: Any) -> list[dict[str, Any]]:
        """Get all blocks that match the given drops

        Args:
            block_drops (Any): the drops to match to

        Returns:
            list[dict[str, Any]]: the list of blocks that match
        """
        return self._get_all_match(
            'blocks',
            self._filter_by('drops', block_drops)
        )

    def get_first_block_by_transparent(
            self, block_transparent: Any) -> dict[str, Any]:
        """Get the block that matches the given transparent

        Args:
            block_transparent (Any): the transparent to match to

        Returns:
            dict[str, Any]: the block that matches
        """
        return self._get_first_match(
            'blocks',
            self._filter_by('transparent', block_transparent)
        )

    def get_blocks_by_transparent(
            self, block_transparent: Any) -> list[dict[str, Any]]:
        """Get all blocks that match the given transparent

        Args:
            block_transparent (Any): the transparent to match to

        Returns:
            list[dict[str, Any]]: the list of blocks that match
        """
        return self._get_all_match(
            'blocks',
            self._filter_by('transparent', block_transparent)
        )

    def get_first_block_by_id(
            self, block_id: Any) -> dict[str, Any]:
        """Get the block that matches the given id

        Args:
            block_id (Any): the id to match to

        Returns:
            dict[str, Any]: the block that matches
        """
        return self._get_first_match(
            'blocks',
            self._filter_by('id', block_id)
        )

    def get_blocks_by_id(
            self, block_id: Any) -> list[dict[str, Any]]:
        """Get all blocks that match the given id

        Args:
            block_id (Any): the id to match to

        Returns:
            list[dict[str, Any]]: the list of blocks that match
        """
        return self._get_all_match(
            'blocks',
            self._filter_by('id', block_id)
        )

    def get_first_block_by_defaultState(
            self, block_defaultState: Any) -> dict[str, Any]:
        """Get the block that matches the given defaultState

        Args:
            block_defaultState (Any): the defaultState to match to

        Returns:
            dict[str, Any]: the block that matches
        """
        return self._get_first_match(
            'blocks',
            self._filter_by('defaultState', block_defaultState)
        )

    def get_blocks_by_defaultState(
            self, block_defaultState: Any) -> list[dict[str, Any]]:
        """Get all blocks that match the given defaultState

        Args:
            block_defaultState (Any): the defaultState to match to

        Returns:
            list[dict[str, Any]]: the list of blocks that match
        """
        return self._get_all_match(
            'blocks',
            self._filter_by('defaultState', block_defaultState)
        )

    def get_first_block_by_hardness(
            self, block_hardness: Any) -> dict[str, Any]:
        """Get the block that matches the given hardness

        Args:
            block_hardness (Any): the hardness to match to

        Returns:
            dict[str, Any]: the block that matches
        """
        return self._get_first_match(
            'blocks',
            self._filter_by('hardness', block_hardness)
        )

    def get_blocks_by_hardness(
            self, block_hardness: Any) -> list[dict[str, Any]]:
        """Get all blocks that match the given hardness

        Args:
            block_hardness (Any): the hardness to match to

        Returns:
            list[dict[str, Any]]: the list of blocks that match
        """
        return self._get_all_match(
            'blocks',
            self._filter_by('hardness', block_hardness)
        )

    def get_food_ids(self) -> list[int]:
        """Get all possible food ids

        Returns:
            list[int]: all the possible food ids
        """
        return list(map(int, (x['id'] for x in self._get_data('foods'))))

    def get_first_food_by_foodPoints(
            self, food_foodPoints: Any) -> dict[str, Any]:
        """Get the food that matches the given foodPoints

        Args:
            food_foodPoints (Any): the foodPoints to match to

        Returns:
            dict[str, Any]: the food that matches
        """
        return self._get_first_match(
            'foods',
            self._filter_by('foodPoints', food_foodPoints)
        )

    def get_foods_by_foodPoints(
            self, food_foodPoints: Any) -> list[dict[str, Any]]:
        """Get all foods that match the given foodPoints

        Args:
            food_foodPoints (Any): the foodPoints to match to

        Returns:
            list[dict[str, Any]]: the list of foods that match
        """
        return self._get_all_match(
            'foods',
            self._filter_by('foodPoints', food_foodPoints)
        )

    def get_first_food_by_stackSize(
            self, food_stackSize: Any) -> dict[str, Any]:
        """Get the food that matches the given stackSize

        Args:
            food_stackSize (Any): the stackSize to match to

        Returns:
            dict[str, Any]: the food that matches
        """
        return self._get_first_match(
            'foods',
            self._filter_by('stackSize', food_stackSize)
        )

    def get_foods_by_stackSize(
            self, food_stackSize: Any) -> list[dict[str, Any]]:
        """Get all foods that match the given stackSize

        Args:
            food_stackSize (Any): the stackSize to match to

        Returns:
            list[dict[str, Any]]: the list of foods that match
        """
        return self._get_all_match(
            'foods',
            self._filter_by('stackSize', food_stackSize)
        )

    def get_first_food_by_displayName(
            self, food_displayName: Any) -> dict[str, Any]:
        """Get the food that matches the given displayName

        Args:
            food_displayName (Any): the displayName to match to

        Returns:
            dict[str, Any]: the food that matches
        """
        return self._get_first_match(
            'foods',
            self._filter_by('displayName', food_displayName)
        )

    def get_foods_by_displayName(
            self, food_displayName: Any) -> list[dict[str, Any]]:
        """Get all foods that match the given displayName

        Args:
            food_displayName (Any): the displayName to match to

        Returns:
            list[dict[str, Any]]: the list of foods that match
        """
        return self._get_all_match(
            'foods',
            self._filter_by('displayName', food_displayName)
        )

    def get_first_food_by_saturation(
            self, food_saturation: Any) -> dict[str, Any]:
        """Get the food that matches the given saturation

        Args:
            food_saturation (Any): the saturation to match to

        Returns:
            dict[str, Any]: the food that matches
        """
        return self._get_first_match(
            'foods',
            self._filter_by('saturation', food_saturation)
        )

    def get_foods_by_saturation(
            self, food_saturation: Any) -> list[dict[str, Any]]:
        """Get all foods that match the given saturation

        Args:
            food_saturation (Any): the saturation to match to

        Returns:
            list[dict[str, Any]]: the list of foods that match
        """
        return self._get_all_match(
            'foods',
            self._filter_by('saturation', food_saturation)
        )

    def get_first_food_by_name(
            self, food_name: Any) -> dict[str, Any]:
        """Get the food that matches the given name

        Args:
            food_name (Any): the name to match to

        Returns:
            dict[str, Any]: the food that matches
        """
        return self._get_first_match(
            'foods',
            self._filter_by('name', food_name)
        )

    def get_foods_by_name(
            self, food_name: Any) -> list[dict[str, Any]]:
        """Get all foods that match the given name

        Args:
            food_name (Any): the name to match to

        Returns:
            list[dict[str, Any]]: the list of foods that match
        """
        return self._get_all_match(
            'foods',
            self._filter_by('name', food_name)
        )

    def get_first_food_by_saturationRatio(
            self, food_saturationRatio: Any) -> dict[str, Any]:
        """Get the food that matches the given saturationRatio

        Args:
            food_saturationRatio (Any): the saturationRatio to match to

        Returns:
            dict[str, Any]: the food that matches
        """
        return self._get_first_match(
            'foods',
            self._filter_by('saturationRatio', food_saturationRatio)
        )

    def get_foods_by_saturationRatio(
            self, food_saturationRatio: Any) -> list[dict[str, Any]]:
        """Get all foods that match the given saturationRatio

        Args:
            food_saturationRatio (Any): the saturationRatio to match to

        Returns:
            list[dict[str, Any]]: the list of foods that match
        """
        return self._get_all_match(
            'foods',
            self._filter_by('saturationRatio', food_saturationRatio)
        )

    def get_first_food_by_id(
            self, food_id: Any) -> dict[str, Any]:
        """Get the food that matches the given id

        Args:
            food_id (Any): the id to match to

        Returns:
            dict[str, Any]: the food that matches
        """
        return self._get_first_match(
            'foods',
            self._filter_by('id', food_id)
        )

    def get_foods_by_id(
            self, food_id: Any) -> list[dict[str, Any]]:
        """Get all foods that match the given id

        Args:
            food_id (Any): the id to match to

        Returns:
            list[dict[str, Any]]: the list of foods that match
        """
        return self._get_all_match(
            'foods',
            self._filter_by('id', food_id)
        )

    def get_first_food_by_effectiveQuality(
            self, food_effectiveQuality: Any) -> dict[str, Any]:
        """Get the food that matches the given effectiveQuality

        Args:
            food_effectiveQuality (Any): the effectiveQuality to match to

        Returns:
            dict[str, Any]: the food that matches
        """
        return self._get_first_match(
            'foods',
            self._filter_by('effectiveQuality', food_effectiveQuality)
        )

    def get_foods_by_effectiveQuality(
            self, food_effectiveQuality: Any) -> list[dict[str, Any]]:
        """Get all foods that match the given effectiveQuality

        Args:
            food_effectiveQuality (Any): the effectiveQuality to match to

        Returns:
            list[dict[str, Any]]: the list of foods that match
        """
        return self._get_all_match(
            'foods',
            self._filter_by('effectiveQuality', food_effectiveQuality)
        )

    def get_first_entity_by_type(
            self, entity_type: Any) -> dict[str, Any]:
        """Get the entity that matches the given type

        Args:
            entity_type (Any): the type to match to

        Returns:
            dict[str, Any]: the entity that matches
        """
        return self._get_first_match(
            'entities',
            self._filter_by('type', entity_type)
        )

    def get_entities_by_type(
            self, entity_type: Any) -> list[dict[str, Any]]:
        """Get all entities that match the given type

        Args:
            entity_type (Any): the type to match to

        Returns:
            list[dict[str, Any]]: the list of entities that match
        """
        return self._get_all_match(
            'entities',
            self._filter_by('type', entity_type)
        )

    def get_first_entity_by_displayName(
            self, entity_displayName: Any) -> dict[str, Any]:
        """Get the entity that matches the given displayName

        Args:
            entity_displayName (Any): the displayName to match to

        Returns:
            dict[str, Any]: the entity that matches
        """
        return self._get_first_match(
            'entities',
            self._filter_by('displayName', entity_displayName)
        )

    def get_entities_by_displayName(
            self, entity_displayName: Any) -> list[dict[str, Any]]:
        """Get all entities that match the given displayName

        Args:
            entity_displayName (Any): the displayName to match to

        Returns:
            list[dict[str, Any]]: the list of entities that match
        """
        return self._get_all_match(
            'entities',
            self._filter_by('displayName', entity_displayName)
        )

    def get_first_entity_by_name(
            self, entity_name: Any) -> dict[str, Any]:
        """Get the entity that matches the given name

        Args:
            entity_name (Any): the name to match to

        Returns:
            dict[str, Any]: the entity that matches
        """
        return self._get_first_match(
            'entities',
            self._filter_by('name', entity_name)
        )

    def get_entities_by_name(
            self, entity_name: Any) -> list[dict[str, Any]]:
        """Get all entities that match the given name

        Args:
            entity_name (Any): the name to match to

        Returns:
            list[dict[str, Any]]: the list of entities that match
        """
        return self._get_all_match(
            'entities',
            self._filter_by('name', entity_name)
        )

    def get_first_entity_by_width(
            self, entity_width: Any) -> dict[str, Any]:
        """Get the entity that matches the given width

        Args:
            entity_width (Any): the width to match to

        Returns:
            dict[str, Any]: the entity that matches
        """
        return self._get_first_match(
            'entities',
            self._filter_by('width', entity_width)
        )

    def get_entities_by_width(
            self, entity_width: Any) -> list[dict[str, Any]]:
        """Get all entities that match the given width

        Args:
            entity_width (Any): the width to match to

        Returns:
            list[dict[str, Any]]: the list of entities that match
        """
        return self._get_all_match(
            'entities',
            self._filter_by('width', entity_width)
        )

    def get_first_entity_by_category(
            self, entity_category: Any) -> dict[str, Any]:
        """Get the entity that matches the given category

        Args:
            entity_category (Any): the category to match to

        Returns:
            dict[str, Any]: the entity that matches
        """
        return self._get_first_match(
            'entities',
            self._filter_by('category', entity_category)
        )

    def get_entities_by_category(
            self, entity_category: Any) -> list[dict[str, Any]]:
        """Get all entities that match the given category

        Args:
            entity_category (Any): the category to match to

        Returns:
            list[dict[str, Any]]: the list of entities that match
        """
        return self._get_all_match(
            'entities',
            self._filter_by('category', entity_category)
        )

    def get_first_entity_by_metadataKeys(
            self, entity_metadataKeys: Any) -> dict[str, Any]:
        """Get the entity that matches the given metadataKeys

        Args:
            entity_metadataKeys (Any): the metadataKeys to match to

        Returns:
            dict[str, Any]: the entity that matches
        """
        return self._get_first_match(
            'entities',
            self._filter_by('metadataKeys', entity_metadataKeys)
        )

    def get_entities_by_metadataKeys(
            self, entity_metadataKeys: Any) -> list[dict[str, Any]]:
        """Get all entities that match the given metadataKeys

        Args:
            entity_metadataKeys (Any): the metadataKeys to match to

        Returns:
            list[dict[str, Any]]: the list of entities that match
        """
        return self._get_all_match(
            'entities',
            self._filter_by('metadataKeys', entity_metadataKeys)
        )

    def get_first_entity_by_internalId(
            self, entity_internalId: Any) -> dict[str, Any]:
        """Get the entity that matches the given internalId

        Args:
            entity_internalId (Any): the internalId to match to

        Returns:
            dict[str, Any]: the entity that matches
        """
        return self._get_first_match(
            'entities',
            self._filter_by('internalId', entity_internalId)
        )

    def get_entities_by_internalId(
            self, entity_internalId: Any) -> list[dict[str, Any]]:
        """Get all entities that match the given internalId

        Args:
            entity_internalId (Any): the internalId to match to

        Returns:
            list[dict[str, Any]]: the list of entities that match
        """
        return self._get_all_match(
            'entities',
            self._filter_by('internalId', entity_internalId)
        )

    def get_first_entity_by_id(
            self, entity_id: Any) -> dict[str, Any]:
        """Get the entity that matches the given id

        Args:
            entity_id (Any): the id to match to

        Returns:
            dict[str, Any]: the entity that matches
        """
        return self._get_first_match(
            'entities',
            self._filter_by('id', entity_id)
        )

    def get_entities_by_id(
            self, entity_id: Any) -> list[dict[str, Any]]:
        """Get all entities that match the given id

        Args:
            entity_id (Any): the id to match to

        Returns:
            list[dict[str, Any]]: the list of entities that match
        """
        return self._get_all_match(
            'entities',
            self._filter_by('id', entity_id)
        )

    def get_first_entity_by_height(
            self, entity_height: Any) -> dict[str, Any]:
        """Get the entity that matches the given height

        Args:
            entity_height (Any): the height to match to

        Returns:
            dict[str, Any]: the entity that matches
        """
        return self._get_first_match(
            'entities',
            self._filter_by('height', entity_height)
        )

    def get_entities_by_height(
            self, entity_height: Any) -> list[dict[str, Any]]:
        """Get all entities that match the given height

        Args:
            entity_height (Any): the height to match to

        Returns:
            list[dict[str, Any]]: the list of entities that match
        """
        return self._get_all_match(
            'entities',
            self._filter_by('height', entity_height)
        )

    def get_recipe_results(self) -> list[str]:
        """Get all the possible results

        Returns:
            list[str]: the list of results
        """
        return list(map(int, self._get_data('recipes').keys()))

    def get_first_recipe_by_result_id(self, result_id: Any) -> dict[str, Any]:
        """Get the first recipe that matches the result_id

        Args:
            result_id (Any): the id to check

        Returns:
            dict[str, Any]: the recipes where the result matches the result_id
        """
        return self._get_data('recipes')[str(result_id)]

    def get_first_recipe_by_ingredients(
            self, recipe_ingredients: Any) -> dict[str, Any]:
        """Get the recipe that matches the given ingredients

        Args:
            recipe_ingredients (Any): the ingredients to match to

        Returns:
            dict[str, Any]: the recipe that matches
        """
        return self._get_first_match(
            'recipes',
            self._filter_by('ingredients', recipe_ingredients)
        )

    def get_recipes_by_ingredients(
            self, recipe_ingredients: Any) -> list[dict[str, Any]]:
        """Get all recipes that match the given ingredients

        Args:
            recipe_ingredients (Any): the ingredients to match to

        Returns:
            list[dict[str, Any]]: the list of recipes that match
        """
        return self._get_all_match(
            'recipes',
            self._filter_by('ingredients', recipe_ingredients)
        )

    def get_first_recipe_by_inShape(
            self, recipe_inShape: Any) -> dict[str, Any]:
        """Get the recipe that matches the given inShape

        Args:
            recipe_inShape (Any): the inShape to match to

        Returns:
            dict[str, Any]: the recipe that matches
        """
        return self._get_first_match(
            'recipes',
            self._filter_by('inShape', recipe_inShape)
        )

    def get_recipes_by_inShape(
            self, recipe_inShape: Any) -> list[dict[str, Any]]:
        """Get all recipes that match the given inShape

        Args:
            recipe_inShape (Any): the inShape to match to

        Returns:
            list[dict[str, Any]]: the list of recipes that match
        """
        return self._get_all_match(
            'recipes',
            self._filter_by('inShape', recipe_inShape)
        )

    def get_first_recipe_by_result(
            self, recipe_result: Any) -> dict[str, Any]:
        """Get the recipe that matches the given result

        Args:
            recipe_result (Any): the result to match to

        Returns:
            dict[str, Any]: the recipe that matches
        """
        return self._get_first_match(
            'recipes',
            self._filter_by('result', recipe_result)
        )

    def get_recipes_by_result(
            self, recipe_result: Any) -> list[dict[str, Any]]:
        """Get all recipes that match the given result

        Args:
            recipe_result (Any): the result to match to

        Returns:
            list[dict[str, Any]]: the list of recipes that match
        """
        return self._get_all_match(
            'recipes',
            self._filter_by('result', recipe_result)
        )
