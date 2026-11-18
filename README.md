# Pedestal

A simple AssetFurnace add-on that makes a round, stepped display stand.

## What it does

Give it a height, width and number of steps and it produces a GLB ready to drop a
model on top of.

## Install

In AssetFurnace:

```bash
./lab addon add pedestal
```

Or, to test a copy that is not on the list yet, from a specific commit:

```bash
./lab addon add --unlisted https://github.com/AssetFurnace/pedestal-addon.git@<commit-hash>
```

## Use

From the studio Add-ons page, or from the CLI:

```bash
./lab addon run pedestal build --input height=0.6 --input width=0.4 --input steps=3 --yes
```

## Learn from it

Pedestal is the smallest add-on we could write. To build your own, see the guide: https://assetfurnace.com/blog/build-an-add-on

## Licence

Apache-2.0
