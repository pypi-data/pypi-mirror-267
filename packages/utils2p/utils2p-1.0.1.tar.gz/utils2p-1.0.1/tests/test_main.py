"""
This module provides unit tests for the functions provided in utils2p.main.
"""

import os.path
import struct
from pathlib import Path

import pytest
import numpy as np

import utils2p
from utils2p.external import tifffile


data_dir = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture
def random_stack():
    """
    This pytest fixture generates a random array of given
    size with uint16 values up to :math:`2^{14}` as generated
    by the Aalazar card of the microscope.

    Parameters
    ----------
    shape : tuple
        Shape of array. Default is (10, 50, 60).

    Returns
    -------
    img_stack : numpy array
        Random array.
    """

    def _random_stack(shape=(10, 50, 60)):
        img_stack = np.random.randint(0, 2 ** 14, shape, dtype=np.uint16)
        return img_stack

    return _random_stack


@pytest.fixture
def random_tif_file(tmpdir, random_stack):
    """
    This pytest factory writes a random stack retuned
    by :func:`.random_stack` to file a tif file and returns
    the path and the matrix.

    Parameters
    ----------
    shape : tuple
        Shape of stack. Default is (10, 50, 60).

    Returns
    -------
    file_path : PosixPath
        Path to tif file.
    random_stack : numpy array
        Matrix of the stack.
    """

    def _random_tif_file(shape=(10, 50, 60)):
        file_path = tmpdir.join("img_stack.tif")
        img_stack = random_stack(shape)
        tifffile.imsave(str(file_path), img_stack)
        return file_path, img_stack

    return _random_tif_file


@pytest.fixture
def random_raw_file(tmpdir, random_stack, metadata_obj):
    """
    This pytest factory writes as random stack to a binary file as it is
    saved by ThorImage in raw data capture mode.

    Parameters
    ----------
    area_mode : int
        Area mode of the acquisition.
    shape : tuple of int
        Shape of a single x-y frame.
    timepoints : int
        Number of timepoints.
    channels : tuple of strings
        Names of the channels.
    n_z : int
        Number of steps in z direction.
    flyback_frames : int
        Number of flyback frames.

    Returns
    -------
    file_path : PosixPath
        Path to binary file.
    metadata_for_raw : Metadata object
        Metadata object with the set parameters.
    images : tuple of numpy arrays
        Each element of the tuple is the acquired stack for a different channel.
    """

    def _random_raw_file(
        area_mode=0,
        shape=(50, 60),
        timepoints=10,
        channels=("ChanA", "ChanB"),
        n_z=1,
        flyback_frames=0,
    ):
        if area_mode == 2 or area_mode == 3:
            new_n_y_pixels = shape[0] / n_z
            assert (
                not new_n_y_pixels % 1
            ), "Invalid test parameter. For kymograph and line the y values has to be divisible by the number of z steps."
            new_n_y_pixels = int(new_n_y_pixels)
            shape = (new_n_y_pixels, shape[1])

        img_stacks = np.zeros(
            (timepoints, n_z + flyback_frames, len(channels)) + shape, dtype=np.uint16
        )
        for t in range(timepoints):
            for i in range(len(channels)):
                img_stacks[t, :n_z, i] = random_stack((n_z,) + shape)
        metadata_for_raw = metadata_obj(
            timepoints=timepoints,
            x_pixels=shape[1],
            y_pixels=shape[0],
            channels=channels,
            n_z=n_z,
            area_mode=area_mode,
        )
        file_path = tmpdir.join("Image_0001_0001.raw")
        sequence = img_stacks.flatten()
        out = bytearray(len(sequence) * 2)
        struct.pack_into(f"<{len(sequence)}H", out, 0, *sequence)
        with open(file_path, "xb") as f:
            f.write(out)
        return (
            file_path,
            metadata_for_raw,
            tuple((np.squeeze(img_stacks[:, :n_z, i]) for i in range(len(channels)))),
        )

    return _random_raw_file


@pytest.fixture
def default_exp_dir(tmpdir):
    tmpdir = Path(tmpdir)
    tmpdir.joinpath("Untitled_001").mkdir()
    tmpdir.joinpath("Untitled_001/Experiment.xml").touch()
    tmpdir.joinpath("Untitled_001/Image_0001_0001.raw").touch()
    tmpdir.joinpath("Untitled_001/ROIMask.raw").touch()
    tmpdir.joinpath("Untitled_001/ROIs.xaml").touch()
    tmpdir.joinpath("Untitled_001/ChanA_Preview.tif").touch()
    tmpdir.joinpath("Untitled_001/ChanB_Preview.tif").touch()
    tmpdir.joinpath("Untitled_001/jpeg/1x").mkdir(parents=True)
    tmpdir.joinpath("sync001").mkdir()
    tmpdir.joinpath("sync001/Episode001.h5").touch()
    tmpdir.joinpath("sync001/ThorRealTimeDataSettings.xml").touch()
    return tmpdir


def test_get_metadata_value(metadata_obj):
    assert (
        metadata_obj().get_metadata_value("Wavelengths", "ChannelEnable", "Set") == "3"
    )


@pytest.mark.parametrize("timepoints", [0, 1, 10])
def test_get_n_time_points(metadata_obj, timepoints):
    assert metadata_obj(timepoints=timepoints).get_n_time_points() == timepoints


@pytest.mark.parametrize("x_pixels", [0, 1, 10])
def test_get_num_x_pixels(metadata_obj, x_pixels):
    assert metadata_obj(x_pixels=x_pixels).get_num_x_pixels() == x_pixels


@pytest.mark.parametrize("y_pixels", [0, 1, 10])
def test_get_num_y_pixels(metadata_obj, y_pixels):
    assert metadata_obj(y_pixels=y_pixels).get_num_y_pixels() == y_pixels


@pytest.mark.parametrize(
    "area_mode,result", [(0, "square"), (1, "rectangle"), (2, "kymograph"), (3, "line")]
)
def test_get_are_mode(metadata_obj, area_mode, result):
    assert metadata_obj(area_mode=area_mode).get_area_mode() == result


def test_wrong_get_area_mode(metadata_obj):
    with pytest.raises(utils2p.InvalidValueInMetaData):
        metadata_obj(area_mode=5).get_area_mode()


@pytest.mark.parametrize("n_z", [0, 1, 10])
def test_get_n_z(metadata_obj, n_z):
    assert metadata_obj(n_z=n_z).get_n_z() == n_z


@pytest.mark.parametrize(
    "channels,result", [(("ChanA", "ChanB"), 2), (("ChanA", "ChanB", "ChanC"), 3)]
)
def test_get_n_channels(metadata_obj, channels, result):
    assert metadata_obj(channels=channels).get_n_channels() == result


@pytest.mark.parametrize("channels", [("ChanA", "ChanB"), ("ChanA", "ChanC")])
def test_get_channels(metadata_obj, channels):
    assert metadata_obj(channels=channels).get_channels() == channels


@pytest.mark.parametrize("pixel_size", [0, 1, 10])
def test_get_pixel_size(metadata_obj, pixel_size):
    assert metadata_obj(pixel_size=pixel_size).get_pixel_size() == pixel_size


@pytest.mark.parametrize("z_step_size", [0, 1, 10])
def test_get_z_step_size(metadata_obj, z_step_size):
    assert metadata_obj(z_step_size=z_step_size).get_z_step_size() == z_step_size


@pytest.mark.parametrize(
    "area_mode,z_step_size,n_z,y_pixels,result",
    [(0, 1, 3, 4, 1), (1, 3, 1, 4, 3), (2, 0.5, 8, 2, 2), (3, 0.1, 200, 10, 2)],
)
def test_get_z_pixel_size(metadata_obj, area_mode, z_step_size, n_z, y_pixels, result):
    assert np.isclose(
        metadata_obj(
            area_mode=area_mode, z_step_size=z_step_size, n_z=n_z, y_pixels=y_pixels
        ).get_z_pixel_size(),
        result,
    )


@pytest.mark.parametrize("dwell_time", [0, 1, 10])
def test_get_dwell_time(metadata_obj, dwell_time):
    assert metadata_obj(dwell_time=dwell_time).get_dwell_time() == dwell_time


@pytest.mark.parametrize(
    "frame_rate,flyback_frames,n_z,result", [(5.5, 3, 2, 1.1), (8.3, 4, 1, 1.66)]
)
def test_get_frame_rate(metadata_obj, frame_rate, flyback_frames, n_z, result):
    assert np.isclose(
        metadata_obj(
            frame_rate=frame_rate, flyback_frames=flyback_frames, n_z=n_z
        ).get_frame_rate(),
        result,
    )


@pytest.mark.parametrize("width", [0, 1, 10])
def test_get_width(metadata_obj, width):
    assert metadata_obj(width=width).get_width() == width


@pytest.mark.parametrize("power", [0, 1, 10])
def test_get_power(metadata_obj, power):
    assert metadata_obj(power=power).get_power_reg1_start() == power


@pytest.mark.parametrize("gain_a", [0, 1, 10])
def test_get_gain_a(metadata_obj, gain_a):
    assert metadata_obj(gain_a=gain_a).get_gain_a() == gain_a


@pytest.mark.parametrize("gain_b", [0, 1, 10])
def test_get_gain_b(metadata_obj, gain_b):
    assert metadata_obj(gain_b=gain_b).get_gain_b() == gain_b


@pytest.mark.parametrize("date", ["12/20/2018 18:33:52", "05/04/2018 07:05:34"])
def test_get_date(metadata_obj, date):
    assert metadata_obj(date=date).get_date_time() == date


def test_load_img(random_tif_file):
    file_path, img_stack = random_tif_file()
    assert np.allclose(utils2p.load_img(file_path), img_stack)


def test_load_stack_batches(random_tif_file):
    file_path, img_stack = random_tif_file()
    substacks = []
    batch_size = 3
    for substack in utils2p.load_stack_batches(file_path, batch_size):
        assert substack.shape[0] <= batch_size
        substacks.append(substack)
    loaded_stack = np.concatenate(substacks, axis=0)
    assert np.allclose(loaded_stack, img_stack)


@pytest.mark.parametrize("patch_size,padding",
        [
            ((2, 2), 1),
            ((5, 5), 1),
            ((5, 1), (3, 1)),
            ((3, 4), (2, 3)),
        ],
)
def test_load_stack_patches(random_tif_file, patch_size, padding):
    file_path, img_stack = random_tif_file()
    reconstructed_stack = np.zeros_like(img_stack)
    for patch, indices, patch_indices in utils2p.load_stack_patches(file_path, patch_size, padding=padding, return_indices=True):
        patch_wo_padding = patch[:,
                                 patch_indices[0][0] : patch_indices[0][1],
                                 patch_indices[1][0] : patch_indices[1][1]
                                ]
        reconstructed_stack[:,
                            indices[0][0] : indices[0][1],
                            indices[1][0] : indices[1][1]
                           ] = patch_wo_padding
    assert np.allclose(reconstructed_stack, img_stack)

@pytest.mark.parametrize(
    "area_mode,shape,timepoints,channels,n_z,flyback_frames",
    [
        (0, (50, 60), 1, ("ChanA",), 1, 0),
        (0, (50, 60), 1, ("ChanA",), 1, 3),
        (0, (50, 60), 1, ("ChanA",), 2, 0),
        (0, (50, 60), 1, ("ChanA",), 2, 3),
        (0, (50, 60), 1, ("ChanA", "ChanB"), 1, 0),
        (0, (50, 60), 1, ("ChanA", "ChanB"), 1, 3),
        (0, (50, 60), 1, ("ChanA", "ChanB"), 2, 0),
        (0, (50, 60), 1, ("ChanA", "ChanB"), 2, 3),
        (0, (50, 60), 8, ("ChanA",), 1, 0),
        (0, (50, 60), 8, ("ChanA",), 1, 3),
        (0, (50, 60), 8, ("ChanA",), 2, 0),
        (0, (50, 60), 8, ("ChanA",), 2, 3),
        (0, (50, 60), 8, ("ChanA", "ChanB"), 1, 0),
        (0, (50, 60), 8, ("ChanA", "ChanB"), 1, 3),
        (0, (50, 60), 8, ("ChanA", "ChanB"), 2, 0),
        (0, (50, 60), 8, ("ChanA", "ChanB"), 2, 3),
        (1, (50, 60), 1, ("ChanA",), 1, 0),
        (1, (50, 60), 1, ("ChanA",), 1, 3),
        (1, (50, 60), 1, ("ChanA",), 2, 0),
        (1, (50, 60), 1, ("ChanA",), 2, 3),
        (1, (50, 60), 1, ("ChanA", "ChanB"), 1, 0),
        (1, (50, 60), 1, ("ChanA", "ChanB"), 1, 3),
        (1, (50, 60), 1, ("ChanA", "ChanB"), 2, 0),
        (1, (50, 60), 1, ("ChanA", "ChanB"), 2, 3),
        (1, (50, 60), 8, ("ChanA",), 1, 0),
        (1, (50, 60), 8, ("ChanA",), 1, 3),
        (1, (50, 60), 8, ("ChanA",), 2, 0),
        (1, (50, 60), 8, ("ChanA",), 2, 3),
        (1, (50, 60), 8, ("ChanA", "ChanB"), 1, 0),
        (1, (50, 60), 8, ("ChanA", "ChanB"), 1, 3),
        (1, (50, 60), 8, ("ChanA", "ChanB"), 2, 0),
        (1, (50, 60), 8, ("ChanA", "ChanB"), 2, 3),
        (2, (50, 60), 1, ("ChanA",), 1, 0),
        (2, (50, 60), 1, ("ChanA",), 1, 3),
        (2, (50, 60), 1, ("ChanA",), 2, 0),
        (2, (50, 60), 1, ("ChanA",), 2, 3),
        (2, (50, 60), 1, ("ChanA", "ChanB"), 1, 0),
        (2, (50, 60), 1, ("ChanA", "ChanB"), 1, 3),
        (2, (50, 60), 1, ("ChanA", "ChanB"), 2, 0),
        (2, (50, 60), 1, ("ChanA", "ChanB"), 2, 3),
        (2, (50, 60), 8, ("ChanA",), 1, 0),
        (2, (50, 60), 8, ("ChanA",), 1, 3),
        (2, (50, 60), 8, ("ChanA",), 2, 0),
        (2, (50, 60), 8, ("ChanA",), 2, 3),
        (2, (50, 60), 8, ("ChanA", "ChanB"), 1, 0),
        (2, (50, 60), 8, ("ChanA", "ChanB"), 1, 3),
        (2, (50, 60), 8, ("ChanA", "ChanB"), 2, 0),
        (2, (50, 60), 8, ("ChanA", "ChanB"), 2, 3),
        (3, (50, 60), 1, ("ChanA",), 1, 0),
        (3, (50, 60), 1, ("ChanA",), 1, 3),
        (3, (50, 60), 1, ("ChanA",), 2, 0),
        (3, (50, 60), 1, ("ChanA",), 2, 3),
        (3, (50, 60), 1, ("ChanA", "ChanB"), 1, 0),
        (3, (50, 60), 1, ("ChanA", "ChanB"), 1, 3),
        (3, (50, 60), 1, ("ChanA", "ChanB"), 2, 0),
        (3, (50, 60), 1, ("ChanA", "ChanB"), 2, 3),
        (3, (50, 60), 8, ("ChanA",), 1, 0),
        (3, (50, 60), 8, ("ChanA",), 1, 3),
        (3, (50, 60), 8, ("ChanA",), 2, 0),
        (3, (50, 60), 8, ("ChanA",), 2, 3),
        (3, (50, 60), 8, ("ChanA", "ChanB"), 1, 0),
        (3, (50, 60), 8, ("ChanA", "ChanB"), 1, 3),
        (3, (50, 60), 8, ("ChanA", "ChanB"), 2, 0),
        (3, (50, 60), 8, ("ChanA", "ChanB"), 2, 3),
    ],
)
def test_load_raw(
    random_raw_file, area_mode, shape, timepoints, channels, n_z, flyback_frames
):
    file_path, metadata, img_stacks = random_raw_file(
        area_mode=area_mode,
        shape=shape,
        timepoints=timepoints,
        channels=channels,
        n_z=n_z,
        flyback_frames=flyback_frames,
    )
    loaded_stacks = utils2p.load_raw(file_path, metadata)
    for i in range(len(channels)):
        # For Kymograph recordings and Line recordings the z steps have to be concatenated along the vertical image axis.
        if (area_mode == 2 or area_mode == 3) and n_z > 1:
            if timepoints > 1:
                list_of_arrays = [
                    img_stacks[i][:, j] for j in range(img_stacks[i].shape[1])
                ]
            else:
                list_of_arrays = [
                    img_stacks[i][j] for j in range(img_stacks[i].shape[0])
                ]
            img_stack = np.concatenate(list_of_arrays, axis=-2)
        else:
            img_stack = img_stacks[i]
        assert np.allclose(
            loaded_stacks[i], img_stack
        ), f"Failed with parameters area_mode={area_mode}, shape={shape}, timepoints={timepoints}, channels={channels}, n_z={n_z}, flyback_frames={flyback_frames}."


def test_load_z_stack():
    metadata = utils2p.Metadata(data_dir / "mouse_kidney_z_stack/Experiment.xml")
    loaded_z_stack = utils2p.load_z_stack(data_dir / "mouse_kidney_z_stack", metadata)
    z_stack = np.load(data_dir / "mouse_kidney_z_stack/z_stack.npy")
    assert np.allclose(
        loaded_z_stack, z_stack
    ), "Failed to load mouse kidney z-stack correctly."

    metadata = utils2p.Metadata(
        data_dir / "mouse_kidney_time_series_z_stack/Experiment.xml"
    )
    loaded_z_stack = utils2p.load_z_stack(
        data_dir / "mouse_kidney_time_series_z_stack", metadata
    )
    z_stack = np.load(data_dir / "mouse_kidney_time_series_z_stack/z_stack.npy")
    assert np.allclose(
        loaded_z_stack, z_stack
    ), "Failed to load mouse kidney time of z-stacks correctly."


@pytest.mark.parametrize(
    "shape",
    [(2, 3, 4), (3, 4, 2, 4), (3, 4, 5, 3, 4), (5, 6, 7, 4, 5, 3), (4, 1, 3, 4)],
)
def test_concatenate_z(random_stack, shape):
    stack = random_stack(shape)
    concatenated = utils2p.concatenate_z(stack)
    assert concatenated.shape[-2] == stack.shape[-2] * stack.shape[-3]
    assert concatenated.ndim == stack.ndim - 1


@pytest.mark.parametrize(
    "shape",
    [
        (3, 4),
        (2, 3, 4),
        (3, 4, 2, 4),
        (3, 4, 5, 3, 4),
        (5, 6, 7, 4, 5, 1),
        (4, 1, 3, 4),
    ],
)
def test_save_img(tmpdir, random_stack, shape):
    stack = random_stack(shape)
    utils2p.save_img(tmpdir / "stack.tif", stack)
    assert os.path.isfile(tmpdir / "stack.tif")

    stack = random_stack(shape).astype(np.float64)
    utils2p.save_img(tmpdir / "stack_float64.tif", stack)
    assert os.path.isfile(tmpdir / "stack_float64.tif")

    stack = random_stack(shape) > 0.5
    utils2p.save_img(tmpdir / "stack_bool.tif", stack)
    assert os.path.isfile(tmpdir / "stack_bool.tif")

    r_stack = random_stack(shape)
    g_stack = random_stack(shape)
    b_stack = random_stack(shape)
    stack = np.stack((r_stack, g_stack, b_stack), axis=len(shape))
    utils2p.save_img(tmpdir / "stack_color.tif", stack, color=True)
    assert os.path.isfile(tmpdir / "stack_color.tif")

    r_stack = random_stack(shape)
    g_stack = random_stack(shape)
    b_stack = random_stack(shape)
    stack = np.stack((r_stack, g_stack, b_stack), axis=len(shape))
    utils2p.save_img(
        tmpdir / "stack_not_full_dynamic.tif",
        stack,
        color=True,
        full_dynamic_range=False,
    )
    assert os.path.isfile(tmpdir / "stack_not_full_dynamic.tif")

    r_stack = random_stack(shape)
    g_stack = random_stack(shape)
    b_stack = random_stack(shape)
    stack = np.stack((r_stack, g_stack, b_stack), axis=len(shape)).astype(np.float)
    utils2p.save_img(
        tmpdir / "stack_not_full_dynamic_float.tif",
        stack,
        color=True,
        full_dynamic_range=False,
    )
    assert os.path.isfile(tmpdir / "stack_not_full_dynamic_float.tif")

    with pytest.raises(ValueError):
        r_stack = random_stack(shape)
        g_stack = random_stack(shape)
        b_stack = random_stack(shape)
        stack = np.stack((r_stack, g_stack, b_stack), axis=len(shape)).astype(
            np.complex
        )
        utils2p.save_img(
            tmpdir / "stack_not_full_dynamic_complex.tif",
            stack,
            color=True,
            full_dynamic_range=False,
        )


def test_find_metadata_file(default_exp_dir):
    directory = str(default_exp_dir)
    assert utils2p.find_metadata_file(directory) == str(
        default_exp_dir.joinpath("Untitled_001/Experiment.xml")
    )
    # create second Experiment.xml file
    default_exp_dir.joinpath("Experiment.xml").touch()
    with pytest.raises(RuntimeError):
        utils2p.find_metadata_file(directory)
    # delete all Experiment.xml files
    default_exp_dir.joinpath("Experiment.xml").unlink()
    default_exp_dir.joinpath("Untitled_001/Experiment.xml").unlink()
    with pytest.raises(FileNotFoundError):
        utils2p.find_metadata_file(directory)


def test_find_sync_file(default_exp_dir):
    directory = str(default_exp_dir)
    assert utils2p.find_sync_file(directory) == str(
        default_exp_dir.joinpath("sync001/Episode001.h5")
    )
    # create second Episode001.h5 file
    default_exp_dir.joinpath("Episode001.h5").touch()
    with pytest.raises(RuntimeError):
        utils2p.find_sync_file(directory)
    # delete all Episode001.h5 files
    default_exp_dir.joinpath("Episode001.h5").unlink()
    default_exp_dir.joinpath("sync001/Episode001.h5").unlink()
    with pytest.raises(FileNotFoundError):
        utils2p.find_sync_file(directory)


def test_find_raw_file(default_exp_dir):
    directory = str(default_exp_dir)
    assert utils2p.find_raw_file(directory) == str(
        default_exp_dir.joinpath("Untitled_001/Image_0001_0001.raw")
    )
    # create second Image_0001_0001.raw file
    default_exp_dir.joinpath("Image_0001_0001.raw").touch()
    with pytest.raises(RuntimeError):
        utils2p.find_raw_file(directory)
    # delete all Image_0001_0001.raw files
    default_exp_dir.joinpath("Image_0001_0001.raw").unlink()
    default_exp_dir.joinpath("Untitled_001/Image_0001_0001.raw").unlink()
    with pytest.raises(FileNotFoundError):
        utils2p.find_raw_file(directory)


def test_load_optical_flow(tmpdir):
    n_timepoints = 10
    opt_flow_data = np.zeros((n_timepoints, 5), dtype=int)
    opt_flow_data[:, 4] = np.arange(n_timepoints, dtype=int)
    opt_flow_data[1, 0] = -1
    opt_flow_data[3, 1] = 1
    opt_flow_data[6, 2] = 2
    opt_flow_data[9, 3] = -3

    file_name = os.path.join(tmpdir, "OpFlow.txt")
    np.savetxt(file_name, opt_flow_data, delimiter=",")

    for smoothing_kernel in [None, np.ones(3) / 3]:
        result = utils2p.load_optical_flow(file_name, 1, 2, 3, 4, smoothing_kernel=smoothing_kernel)
        assert len(result["sensor0"]["x"]) == n_timepoints
        assert len(result["sensor0"]["y"]) == n_timepoints
        assert len(result["sensor1"]["x"]) == n_timepoints
        assert len(result["sensor1"]["y"]) == n_timepoints
        assert result["sensor0"]["gain_x"] == 1
        assert result["sensor0"]["gain_y"] == 2
        assert result["sensor1"]["gain_x"] == 3
        assert result["sensor1"]["gain_y"] == 4
        assert len(result["vel_pitch"]) == n_timepoints
        assert len(result["vel_yaw"]) == n_timepoints
        assert len(result["vel_roll"]) == n_timepoints

    with pytest.raises(ValueError):
        kernel_length = n_timepoints + 1
        result = utils2p.load_optical_flow(file_name, 1, 2, 3, 4, smoothing_kernel=np.ones(kernel_length) / kernel_length)
